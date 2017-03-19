from flask import (
        abort,
        Blueprint,
        jsonify,
        make_response,
        request,
        )
from flask_jwt_extended import jwt_required, get_jwt_identity

from fnote.blueprints.user.models import User
from fnote.blueprints.note.models import Note


note = Blueprint('note', __name__)


@note.route('/api/v1.0/notes', methods=['GET', 'POST'])
@jwt_required
def note_no_id():
    """Gets all notes from specific user (determined by id from JWT) or posts
    new note.
    :return: JSON response including array of notes.
    """
    email = get_jwt_identity()
    u = User.find_by_identity(email)
    if request.method == 'GET':
        notes = u.get_notes()
        data = []
        for n in notes:
            data.append(n.to_dict())
        return make_response(jsonify({'notes': data, 'statusCode': 200}), 200)
    elif request.method == 'POST':
        try:
            title = request.json['title']
            text = request.json['text']
            n = Note(u.id, title, text).save()
            note_data = n.to_dict()
            data = {'message': 'Note created',
                    'statusCode': 201,
                    'note': note_data}
            return make_response(jsonify(data), 201)
        except KeyError:
            data = {'error': 'Missing parameters in JSON data',
                    'statusCode': 400}
            return make_response(jsonify(data), 400)
        except TypeError:
            data = {'error': 'Missing JSON data', 'statusCode': 400}
            return make_response(jsonify(data), 400)


@note.route('/api/v1.0/notes/<n_id>', methods=['GET', 'DELETE', 'PUT'])
@jwt_required
def note_by_id(n_id):
    """Gets, deletes, or updates single note. Note's owner is checked against
    identity from JWT.
    :return: JSON response.
    """
    email = get_jwt_identity()
    u = User.find_by_identity(email)
    n = Note.find_by_id(n_id)
    if not n:
        data = {'error': 'No note found for that id', 'statusCode': 404}
        return make_response(jsonify(data), 404)
    if n not in u.notes:
        data = {'error': u.email + 'does not have access to that note',
                'statusCode': 403}
        return make_response(jsonify(data), 403)
    if request.method == 'GET':
        data = {'title': n.title, 'text': n.text, 'id': n.id}
        return make_response(jsonify(data), 200)
    elif request.method == 'DELETE':
        data = {'message': 'Note {0} deleted'.format(n.id), 'statusCode': 200}
        n.delete()
        return make_response(jsonify(data), 200)
    elif request.method == 'PUT':
        new_data = request.json
        if not new_data:
            data = {'error': 'Missing JSON data', 'statusCode': 400}
            return make_response(jsonify(data), 400)
        new_text = new_data.get('text', '')
        new_title = new_data.get('title', '')
        if not new_text and not new_title:
            data = {'error': "Missing parameters in JSON data.\n\
                    Valid parameters: 'title', 'text'", 'statusCode': 400}
            return make_response(jsonify(data), 400)
        if new_text and new_text != n.text:
            n.update_text(new_text)
        if new_title and new_title != n.title:
            n.update_title(new_title)
        n_data = n.to_dict()
        data = {'message': 'Note updated', 'note': n_data, 'statusCode': 200}
        return make_response(jsonify(data), 200)
