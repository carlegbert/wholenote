from flask import url_for


class TestPage(object):
    def test_home_page(self, client):
        response = client.get(url_for('page.home'))
        assert response.status_code == 200
