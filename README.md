[Wholenote](https://wholenoteapp.com "Wholenote") is a [Flask](http://flask.pocoo.org "Flask")-powered RESTful API for storing plaintext notes.

Written by [Carl Egbert](http://www.carlegbert.com) - [egbertcarl@gmail.com](mailto:egbertcarl@gmail)


### Authorization

Wholenote uses access and refresh tokens to handle authentication, via [flask-jwt-extended](https://github.com/vimalloc/flask-jwt-extended).
Access tokens are short-lived (15 minutes, in this case) JSON web tokens that are used to access, create, or modify protected data.
Once the access token expires, a refresh token will need to be used to obtain a new one. A succesful login request will return both an access
and a refresh token. The refresh token should be securely stored by the client. More explanation is provided in the API endpoint documentation.

### API Endpoints

See documentation [here](API_ENDPOINTS.md)


#### Running locally
* You will need postgresql, python3, and virtualenv installed
* Create dev and test postgres databases `fnote` and `fnote_test`
* Rename `fnote/config/settings.py.example` to `fnote/config/settings.py` and change variable values in it as needed
* `$ virtualenv -p /usr/bin/python3 venv`
* `$ . venv/bin/activate`
* `$ pip install -r requirements.txt`
* `$ python fnote/grun.py` to run locally with gunicorn. Hosted at http://localhost:9000

#### Running tests:

* py.test -p no:cacheprovider fnote
