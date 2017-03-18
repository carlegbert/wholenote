from flask import Blueprint, render_template


index = Blueprint('index', __name__, template_folder='templates')


@index.route('/')
@index.route('/index')
@index.route('/home')
def home():
    return render_template('index/index.html')
