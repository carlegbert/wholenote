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
