import pytest

from fnote.blueprints.user.models import User
from fnote.blueprints.user.exceptions import (
        UserExistsError,
        UserNotFoundError,
        WrongPasswordError
        )


class TestUser(object):
    def test_find_by_identity(self, db):
        found_user = User.find_by_identity('testuser@localhost')
        assert found_user.email == 'testuser@localhost'

    def test_find_by_identity_fails(self, db):
        found_user = User.find_by_identity('nessie@lochness')
        assert not found_user

    def test_pw_not_plaintext(self, db):
        found_user = User.find_by_identity('testuser@localhost')
        assert found_user.password != 'hunter2'

    def test_register_new_user(self, db):
        new_user = User.register(email='testuser2@localhost',
                                 password='hunter2')
        found_user = User.find_by_identity('testuser2@localhost')
        assert new_user
        assert new_user == found_user

    def test_register_duplicate_email(self, db):
        with pytest.raises(UserExistsError) as exception:
            User.register(email='testuser@localhost',
                          password='hunter2')
        assert 'testuser@localhost' in str(exception)

    def test_check_pw_hash(self, db):
        test_user = User.find_by_identity('testuser@localhost')
        result = test_user.check_password('hunter2')
        assert result

    def test_wrong_pw_fails(self, db):
        test_user = User.find_by_identity('testuser@localhost')
        result = test_user.check_password('hunter1')
        assert not result

    def test_update_password(self, db):
        test_user = User.find_by_identity('testuser@localhost')
        test_user.update_password('hunter1')
        check_pw_result = test_user.check_password('hunter1')
        check_old_pw_result = test_user.check_password('hunter2')
        assert check_pw_result
        assert not check_old_pw_result

    def test_update_email_fails(self, db):
        new_user = User.register(email='testuser3@localhost',
                                 password='hunter2')
        with pytest.raises(UserExistsError) as exception:
            new_user.update_email('testuser@localhost')
        assert 'testuser@localhost' in str(exception)

    def test_update_user_email(self, db):
        test_user = User.find_by_identity('testuser@localhost')
        test_user.update_email('new_email@localhost')
        found_user = User.find_by_identity('new_email@localhost')
        assert found_user
        assert found_user.email == 'new_email@localhost'

    def test_get_jwt_success(self, db):
        User.register(email='jwt_user@localhost', password='hunter2')
        jwt = User.get_jwt('jwt_user@localhost', 'hunter2')
        assert jwt

    def test_get_jwt_bad_pw(self, db):
        User.register(email='jwt_bad_pw@localhost', password='hunter2')
        with pytest.raises(WrongPasswordError) as exception:
            User.get_jwt('jwt_bad_pw@localhost', 'hunter1')
        assert 'jwt_bad_pw@localhost' in str(exception)

    def test_get_jwt_no_user(self, db):
        with pytest.raises(UserNotFoundError) as exception:
            User.get_jwt('bigfoot@pnw', 'hunter2')
        assert 'bigfoot@pnw' in str(exception)
