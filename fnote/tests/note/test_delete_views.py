from fnote.tests.json_helpers import get_json


URL = '/api/v1.0/notes'


class TestDeleteNoteViews(object):
    # Tests with bad authorization, wrong note id, etc are redundant with GET
    # tests since they use the same view, so they are not repeated here.
    def test_delete_note(self, client, unfresh_token, session, note):
        url = '{0}/{1}'.format(URL, note.title)
        auth = {'Authorization': 'Bearer {0}'.format(unfresh_token)}
        response = client.delete(url, headers=auth)
        response_data = get_json(response)
        assert response.status_code == 200
        assert response_data['msg'] == 'Note {0} deleted'.format(note.title)

    def test_delete_refresh(self, client, refresh_token, session, note):
        url = '{0}/{1}'.format(URL, note.title)
        auth = {'Authorization': 'Bearer {0}'.format(refresh_token)}
        refresh = client.post('/api/v1.0/refresh', headers=auth)
        unfresh_tkn = get_json(refresh)['access_token']
        auth = {'Authorization': 'Bearer {0}'.format(unfresh_tkn)}
        response = client.delete(url, headers=auth)
        response_data = get_json(response)
        assert response.status_code == 200
        assert response_data['msg'] == 'Note {0} deleted'.format(note.title)
