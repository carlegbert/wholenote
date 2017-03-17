from fnote.blueprints.user.models import User
from fnote.blueprints.note.models import Note
from fnote.tests.json_helpers import get_json


URL = '/api/v1.0/notes'


class TestGetNoteViews(object):
    def test_get_notes_for_user(self, client, db):
        u = User.register(email='notetester@localhost', password='hunter2')
        n = Note(u.id, 'note title', 'note text').save()
        jwt = User.get_jwt(email=u.email, pw_plain='hunter2')
        auth = {'Authorization': 'Bearer {0}'.format(jwt)}
        response = client.get(URL, headers=auth)
        response_data = get_json(response)
        assert response_data['notes']
        assert response_data['notes'][str(n.id)]
        assert response_data['notes'][str(n.id)]['text'] == n.text
        assert response.status_code == 200

    def test_get_notes_bad_jwt(self, client, db):
        bad_jwt_str = 'thisisnotavalidJWTstring'
        auth = {'Authorization': 'Bearer {0}'.format(bad_jwt_str)}
        response = client.get(URL, headers=auth)
        assert response.status_code == 422

    def test_get_notes_no_jwt(self, client, db):
        response = client.get(URL)
        assert response.status_code == 401

    def test_get_single_note(self, client, db):
        u = User.register(email='notetester2@localhost', password='hunter2')
        n = Note(u.id, 'note title', 'note text').save()
        jwt = User.get_jwt(u.email, 'hunter2')
        auth = {'Authorization': 'Bearer {0}'.format(jwt)}
        url = '{0}/{1}'.format(URL, n.id)
        response = client.get(url, headers=auth)
        response_data = get_json(response)
        assert response.status_code == 200
        assert response_data
        assert response_data['id'] == n.id

    def test_single_note_bad_jwt(self, client, db):
        u = User.register(email='notetester3@localhost', password='hunter2')
        n = Note(u.id, 'note title', 'note text').save()
        bad_jwt_str = 'thisisnotavalidJWTstring'
        auth = {'Authorization': 'Bearer {0}'.format(bad_jwt_str)}
        url = '{0}/{1}'.format(URL, n.id)
        response = client.get(url, headers=auth)
        assert response.status_code == 422

    def test_single_note_wrong_jwt(self, client, db):
        u = User.register(email='notetester4@localhost', password='hunter2')
        u_2 = User.register(email='wronguser@localhost', password='hunter2')
        n = Note(u.id, 'note title', 'note text').save()
        jwt = User.get_jwt(u_2.email, 'hunter2')
        auth = {'Authorization': 'Bearer {0}'.format(jwt)}
        url = '{0}/{1}'.format(URL, n.id)
        response = client.get(url, headers=auth)
        response_data = get_json(response)
        assert response.status_code == 403
        assert u_2.email in response_data['error']

    def test_single_note_no_jwt(self, client, db):
        u = User.register(email='notetester5@localhost', password='hunter2')
        n = Note(u.id, 'note title', 'note text').save()
        url = '{0}/{1}'.format(URL, n.id)
        response = client.get(url)
        assert response.status_code == 401

    def test_single_note_bad_id(self, client, db):
        u = User.register(email='notetester6@localhost', password='hunter2')
        n = Note(u.id, 'note title', 'note text').save()
        nid = n.id + 1
        jwt = User.get_jwt(u.email, 'hunter2')
        auth = {'Authorization': 'Bearer {0}'.format(jwt)}
        url = '{0}/{1}'.format(URL, nid)
        response = client.get(url, headers=auth)
        assert response.status_code == 404
