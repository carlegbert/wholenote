import pytest

from fnote.blueprints.user.models import User
from fnote.blueprints.user.exceptions import (
        UserExistsError,
        UserNotFoundError,
        WrongPasswordError
        )


class TestUser(object):
    def test_find_by_identity(self, db, user):
        found_user = User.find_by_identity(user.email)
        assert found_user == user

    def test_find_by_identity_fails(self, db):
        found_user = User.find_by_identity('nessie@lochness')
        assert not found_user

    def test_pw_not_plaintext(self, db, user):
        assert user.password != 'hunter2'

    def test_register_new_user(self, db, session):
        user_num = len(User.query.all())
        User.register(email='testuser2@localhost', password='hunter2')
        new_user_num = len(User.query.all())
        assert new_user_num == user_num + 1

    def test_register_duplicate_email(self, db):
        with pytest.raises(UserExistsError) as exception:
            User.register(email='testuser@localhost', password='hunter2')
        assert 'testuser@localhost' in str(exception)

    def test_check_pw_hash(self, db, user):
        result = user.check_password('hunter2')
        assert result

    def test_wrong_pw_fails(self, db, user):
        result = user.check_password('hunter1')
        assert not result

    def test_update_password(self, db, user, session):
        user.update_password('hunter1')
        check_pw_result = user.check_password('hunter1')
        check_old_pw_result = user.check_password('hunter2')
        assert check_pw_result
        assert not check_old_pw_result

    def test_update_email_fails(self, db, session):
        new_user = User.register(email='updatefail@localhost',
                                 password='hunter2')
        with pytest.raises(UserExistsError) as exception:
            new_user.update_email('testuser@localhost')
        assert 'testuser@localhost' in str(exception)

    def test_update_user_email(self, db, user, session):
        user.update_email('new_email@localhost')
        found_user = User.find_by_identity('new_email@localhost')
        failed_found_user = User.find_by_identity('testuser@localhost')
        assert found_user
        assert found_user.email == 'new_email@localhost'
        assert not failed_found_user

    def test_get_jwt(self, db, user):
        jwt = user.get_jwt()
        assert jwt
