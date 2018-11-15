from flask import Blueprint, jsonify, request, abort
from wilson.blueprints.api.models import Reply
from wilson.blueprints.api.forms import UserReplyForm

api = Blueprint('api', __name__)


@api.route('/wilson/api/v1/users/replies', methods=['POST'])
@api.route('/wilson/api/v1/users/replies/<user_id>', methods=['GET'])
def user_answer(user_id=None):
    form = UserReplyForm(next=request.args.get('next'))

    if form.validate_on_submit():
        r = Reply()
        msg = form.message.data
        r.message = msg
        r.save()
        print('[userAnswer] saved !')
        response = jsonify({
            'message': msg,
            'result': 'success'
        })
        response.status_code = 201
        return response
    else:
        print('user response with id:  '+user_id)
        #  return reply list
        abort(404)


@api.route('/wilson/api/v1/feedback/<feedback_id>', methods=['GET'])
def get_feedback(feedback_id=None):
    print('[get_feedback] ')
    response = jsonify({
        'message': 'some feedback',
        'result': 'success',
        'feedback_id': feedback_id
    })
    response.status_code = 201
    return response
