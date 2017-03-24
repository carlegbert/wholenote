import pytest

from fnote.blueprints.user.models import User
from fnote.blueprints.user.exceptions import UserExistsError


class TestUser(object):
    def test_find_by_identity(self, db, user):
        found_user = User.find_by_identity(user.email)
        assert found_user == user

    def test_find_by_identity_fails(self, db):
        found_user = User.find_by_identity('nessie@lochness')
        assert not found_user

    def test_pw_not_plaintext(self, db, user):
        assert user.password != 'hunter2password'

    def test_register_new_user(self, db, session):
        user_num = len(User.query.all())
        User.register(email='testuser2@localhost', password='hunter2password')
        new_user_num = len(User.query.all())
        assert new_user_num == user_num + 1

    def test_register_duplicate_email(self, db):
        with pytest.raises(UserExistsError) as exception:
            User.register(email='testuser@localhost',
                          password='hunter2password')
        assert 'testuser@localhost' in str(exception)

    def test_check_pw_hash(self, db, user):
        result = user.check_password('hunter2password')
        assert result

    def test_wrong_pw_fails(self, db, user):
        result = user.check_password('hunter1')
        assert not result

    def test_update_password(self, db, user, session):
        user.update_password('hunter1')
        check_pw_result = user.check_password('hunter1')
        check_old_pw_result = user.check_password('hunter2password')
        assert check_pw_result
        assert not check_old_pw_result

    def test_update_email_fails(self, db, session):
        new_user = User.register(email='updatefail@localhost',
                                 password='hunter2password')
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

    def test_get_refresh_token(self, db, user):
        jwt = user.get_refresh_token()
        assert jwt

    def test_get_unfresh_token(self, db, user):
        jwt = user.get_access_token()
        assert jwt

    def test_get_fresh_token(self, db, user):
        jwt = user.get_access_token(True)
        assert jwt

    def test_tokens_different(self, db, user):
        unfresh = user.get_access_token()
        fresh = user.get_access_token(True)
        refresh = user.get_refresh_token()
        assert fresh != unfresh
        assert fresh != refresh
        assert unfresh != refresh

    def test_get_refresh_tracked(self, db, user):
        old_login_count = user.login_count
        old_login_date = user.last_login
        user.get_refresh_token()
        new_login_count = user.login_count
        new_login_date = user.last_login
        assert old_login_count != new_login_count
        assert old_login_date != new_login_date

    def test_mark_verified(self, db, session):
        u = User.register(email='testverify@localhost', password='hunter2')
        ver_before = u.verified_email
        u.verify_email()
        ver_after = u.verified_email
        assert not ver_before
        assert ver_after
