from flask import url_for
from flask_mail import Message

from fnote.extensions import mail, url_sts


def send_confirmation_message(email):
    """Sends email to user containing email verification link
    :param email: User email address
    :return: None
    """
    msg = Message('Please verify your email address')
    sts_token = url_sts.dumps(['verify_email', email])
    url = url_for('user.verify', tkn=sts_token)
    msg.html = "Click <a href={0}>here</a> or paste {0} into your browser's \
        address bar to verify your account.".format(url)
    msg.add_recipient(email)
    mail.send(msg)


def send_password_reset(email):
    """Sends special time-sensitive token to user allowing password
    to be reset
    :param email: User email address
    :return: None
    """
    msg = Message('Password reset link')
    # generate password reset url/token
    msg.body = 'Password reset token will go here'
    msg.add_recipient(email)
    mail.send(msg)
