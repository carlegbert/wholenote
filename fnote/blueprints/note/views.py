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


@note.route('/api/v1.0/notes', methods=['GET'])
@jwt_required
def get_notes():
    """Gets all notes from specific user (determined by id from JWT)
    :return: JSON response including array of notes.
    """
    email = get_jwt_identity()
    u = User.find_by_identity(email)
    notes = u.get_notes()
    data = {}
    for n in notes:
        data[str(n.id)] = {'title': n.title, 'text': n.text, 'id': n.id}
    return make_response(jsonify({'notes': data, 'statusCode': 200}), 200)


@note.route('/api/v1.0/notes/<n_id>', methods=['GET', 'DELETE'])
@jwt_required
def get_single_note(n_id):
    """Gets single note. Note's owner is checked against
    identity from JWT.
    :return: JSON response including data from found note.
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
