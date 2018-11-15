from threading import Lock
from celery import Celery
from flask import Flask, jsonify, json
from flask_socketio import SocketIO, emit, join_room, leave_room, send, rooms
from wilson.blueprints.page import page
from wilson.blueprints.api import api
from wilson.blueprints.contact import contact
from wilson.blueprints.user import user
from wilson.blueprints.user.models import User
from wilson.extensions import (
    debug_toolbar,
    mail,
    csrf,
    db,
    login_manager
)
# save user reply
from wilson.blueprints.api.forms import UserReplyForm
from wilson.blueprints.api.models import Reply

#  TODO: delete client_list
client_list = []

async_mode = "eventlet"
thread = None
thread_lock = Lock()

CELERY_TASK_LIST = [
    'wilson.blueprints.contact.tasks',
    'wilson.blueprints.user.tasks',
]


def create_app(settings_override=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    socketio = SocketIO(app, async_mode=async_mode, manage_session=False)

    @socketio.on('connect', namespace='/test')
    def connected():
        print('connected')
    #     show  wilson 1st question

    def get_first_item(list):
        if list:
            return list[0]

    def messageReceived(methods=['GET', 'POST']):
        print('message was received!!!')

    def save_user_reply(json):
        print('[home] post validate_on_submit')
        r = Reply()
        r.question_id = json['question_id']
        r.user_id = json['user_id']
        r.feedback_id = json['feedback_id']
        r.message = json['message']
        r.save()
        return None

    @socketio.on('user_answer_event', namespace='/test')
    def handle_user_answer_event(json_data, methods=['GET', 'POST']):
        room_ids = rooms()
        room_id = get_first_item(room_ids)
        msg = json_data['message']
        data = {
            'question_id': '0',
            'user_id': room_id,
            'feedback_id': '0',
            'message': msg}
        # store reply
        save_user_reply(data)
        emit('my response', msg, callback=messageReceived, namespace='/test')

    def userJoined():
        print('[userJoined] new user joined')

    @socketio.on('join', namespace='/test')
    def on_join(data):
        username = data['username']
        print('[join] joined room number ' + str())

    @socketio.on('leave', namespace='/test')
    def on_leave(data):
        username = data['username']
        room = data['room']
        print('[leave] left room number ' + room)
        leave_room(room)
        send(username + ' has left the room.', room=room)

    # login = LoginManager(app)
    # Session(app)

    app.register_blueprint(page)
    app.register_blueprint(contact)
    app.register_blueprint(user)
    app.register_blueprint(api)
    extensions(app)
    authentication(app, User)

    if __name__ == '__main__':
        socketio.run(app)

    return app


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    task_base = celery.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def authentication(app, user_model):
    """
    Initialize the Flask-Login extension (mutates the app passed in).

    :param app: Flask application instance
    :param user_model: Model that contains the authentication information
    :type user_model: SQLAlchemy model
    :return: None
    """
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)


# def background_thread():
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('my response',
#                       {'data': 'Server generated event', 'count': count},
#                       namespace='/test')

def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    return None
