from flask import Blueprint, render_template, request, jsonify, session

page = Blueprint('page', __name__, template_folder='templates')

async_mode = 'eventlet'


@page.route('/')
def home():
    #  add response cookie
    # return render_template('page/home.html', async_mode=async_mode)
    return render_template('page/home.html')


@page.route('/terms')
def terms():
    return render_template('page/terms.html')


@page.route('/privacy')
def privacy():
    return render_template('page/privacy.html')
