from base64 import b64encode
import re

from ..json_helpers import get_json, post_json


LOGIN_URL = '/api/v1.0/login'
REGISTER_URL = '/api/v1.0/register'


class TestMultipleViews(object):
    def test_register_login_no_verify(self, client, session):
        post_data = {'email': 'viewtest@localhost', 'password': 'hunter2pswd'}
        reg_response = post_json(client, REGISTER_URL, post_data)
        authstr = b64encode(b'viewtest@localhost:hunter2pswd').decode('utf-8')
        auth = {'Authorization': 'Basic {0}'.format(authstr)}
        login_response = client.post(LOGIN_URL, headers=auth)
        login_response_data = get_json(login_response)

        assert reg_response.status_code == 200
        assert login_response.status_code == 403
        assert login_response_data['msg'] == 'Unverified email address'

    def test_register_login_with_verify(self, client, session, mail):
        post_data = {'email': 'verify@localhost', 'password': 'hunter2pswd'}
        with mail.record_messages() as outbox:
            reg_response = post_json(client, REGISTER_URL, post_data)
            mail_res = outbox[0]
        found_url = re.findall('<a href="?\'?([^"\'>]*)', mail_res.html)
        verify_response = client.get(found_url[0])

        authstr = b64encode(b'verify@localhost:hunter2pswd').decode('utf-8')
        auth = {'Authorization': 'Basic {0}'.format(authstr)}
        login_response = client.post(LOGIN_URL, headers=auth)

        assert reg_response.status_code == 200
        assert verify_response.status_code == 200
        assert login_response.status_code == 200
