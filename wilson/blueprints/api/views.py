from flask import Blueprint, request
from wilson.blueprints.api.models import Reply
from wilson.blueprints.api.forms import UserReplyForm

api = Blueprint('api', __name__)

@api.route('/wilson/api//v1.0/users/answer', methods=['POST'])
def userAnswer():
    form = UserReplyForm()

    if form.validate_on_submit():
        r = Reply()
        #  TODO: id 자동 countiong 생성
        r.user_id = form.user_id
        r.question_id = form.question_id
        r.feedback_id = form.feedback_id
        r.message = form.message
        r.save()
        print('userAnswer saved !')