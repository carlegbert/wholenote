from flask import (
        abort,
        Blueprint,
        jsonify,
        make_response,
        request,
        )
from flask_jwt_extended import jwt_required

from fnote.blueprints.note.models import Note


note = Blueprint('note', __name__)


@note.route('/api/v1.0/note/<keyphrase>', methods=['GET', 'POST'])
def single_note():
    abort(500)


@jwt_required
@note.route('/api/v1.0/note/all', methods=['GET'])
def all_notes():
    abort(500)
