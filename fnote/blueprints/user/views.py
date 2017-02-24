from flask import Blueprint, render_template


user = Blueprint('user', __name__, template_folder='templates')


@user.route('/login')
def login():
    return render_template('user/login.html')
