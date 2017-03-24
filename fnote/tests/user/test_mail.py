from ..json_helpers import post_json
from fnote.blueprints.user.mail import send_confirmation_message, \
        send_password_reset


class TestMail(object):
    def test_verification_mail_sends(self, mail):
        with mail.record_messages() as outbox:
            send_confirmation_message('testuser@localhost')
            assert len(outbox) == 1
            assert outbox[0].subject == 'Please verify your email address'

    def test_reset_password_mail_sends(self, mail):
        with mail.record_messages() as outbox:
            send_password_reset('testuser@localhost')
            assert len(outbox) == 1
            assert outbox[0].subject == 'Password reset link'

    def test_register_sends_confirm_email(self, client, session, mail):
        post_data = {'email': 'verifyme@localhost', 'password': 'hunter2pswd'}
        with mail.record_messages() as outbox:
            post_json(client, 'api/v1.0/register', post_data)
            assert len(outbox) == 1

    def test_bad_verify_url_fails(self, client):
        response = client.get('verify/notarealtoken')
        assert 'FAIL' in str(response.data)
        assert response.status_code == 200

    def test_verify_url_no_tkn_fails(self, client):
        response = client.get('verify')
        assert response.status_code == 404
