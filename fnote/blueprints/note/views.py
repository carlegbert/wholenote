from flask import (
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
        return make_response(jsonify({'notes': data}), 200)
    elif request.method == 'POST':
        try:
            title = request.json['title']
            if len(title) > 255:
                title = title[:255]
            text = request.json['text']
            n = Note(u.id, title, text).save()
            note_data = n.to_dict()
            data = {'msg': 'Note created', 'note': note_data}
            return make_response(jsonify(data), 201)
        except KeyError:
            data = {'msg': 'Missing parameters in JSON data'}
            return make_response(jsonify(data), 400)
        except TypeError:
            data = {'msg': 'Missing JSON data'}
            return make_response(jsonify(data), 400)


@note.route('/api/v1.0/notes/<title_id>', methods=['GET', 'DELETE', 'PUT'])
@jwt_required
def note_by_title_id(title_id):
    """Gets, deletes, or updates single note. Note's owner is checked against
    identity from JWT.
    :return: JSON response.
    """
    email = get_jwt_identity()
    u = User.find_by_identity(email)  # TODO: figure out if this can fail??
    n = Note.find_by_title_id(title_id, u)
    if not n:
        data = {'msg': 'No note found for that id'}
        return make_response(jsonify(data), 404)
    if request.method == 'GET':
        data = n.to_dict()
        return make_response(jsonify(data), 200)
    elif request.method == 'DELETE':
        data = {'msg': 'Note {0} deleted'.format(title_id)}
        n.delete()
        return make_response(jsonify(data), 200)
    elif request.method == 'PUT':
        return put_note(n, request)


def put_note(note, request):
    """Modify note. Called by .../notes/<title_id> view.
    :return: JSON response
    """
    new_data = request.json
    if not new_data:
        data = {'msg': 'Missing JSON data'}
        return make_response(jsonify(data), 400)
    new_text = new_data.get('text', '')
    new_title = new_data.get('title', '')
    if len(new_title) > 255:
        new_title = new_title[:255]
    if not new_text and not new_title:
        data = {'msg': "Missing parameters in JSON data.\n\
                Valid parameters: 'title', 'text'"}
        return make_response(jsonify(data), 400)
    if new_text and new_text != note.text:
        note.update_text(new_text)
    if new_title and new_title != note.title:
        note.update_title(new_title)
    n_data = note.to_dict()
    data = {'msg': 'Note updated', 'note': n_data}
    return make_response(jsonify(data), 200)
