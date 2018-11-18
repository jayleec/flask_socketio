from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify, json
from wilson.blueprints.api.forms import UserReplyForm
from lib.safe_next_url import safe_next_url
from wilson.blueprints.api.models import Reply
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user)

page = Blueprint('page', __name__, template_folder='templates')
async_mode = 'eventlet'


@page.route('/', methods=['GET'])
def home():
    form = UserReplyForm(next=request.args.get('next'))

    #     return redirect(url_for('api.add_feedback'))
    # if form.validate_on_submit():
    #     r = Reply()
    #     msg = form.message.data
    #     r.message = msg
    #     r.save()
    #     print('[userAnswer] saved !')
    #     response = jsonify({
    #         'message': msg,
    #         'result': 'success'
    #     })
    #     response.status_code = 201
    #     return render_template('page/home.html', async_mode=async_mode, form=form, test_data=msg)

    return render_template('page/home.html', async_mode=async_mode, form=form)


@page.route('/terms')
def terms():
    return render_template('page/terms.html')


@page.route('/privacy')
@login_required
def privacy():
    return render_template('page/privacy.html')
