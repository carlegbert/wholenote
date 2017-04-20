from flask import Blueprint, render_template


page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
@page.route('/index')
@page.route('/home')
def home():
    # in prod this could return an SPA made with react, angular, etc,
    # or the page blueprint could be deleted entirely and the static
    # page could be served directly by nginx or apache.
    return render_template('page/index.html')
