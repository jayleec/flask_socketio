from threading import Lock
from celery import Celery
from flask import Flask, redirect, url_for
from flask_session import Session
from itsdangerous import URLSafeTimedSerializer
from flask_socketio import SocketIO, emit, join_room, leave_room, send, rooms
from wilson.blueprints.page import page
from wilson.blueprints.api import api
from wilson.blueprints.contact import contact
from wilson.blueprints.api.models import Reply, Users
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user)
from wilson.extensions import (
    debug_toolbar,
    mail,
    csrf,
    db,
    login_manager
)

async_mode = "eventlet"
thread = None
thread_lock = Lock()

CELERY_TASK_LIST = [
    'wilson.blueprints.contact.tasks',
    # 'wilson.blueprints.user.tasks',
]

def create_app(settings_override=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    socketio = SocketIO(app, async_mode=async_mode, manage_session=False)

    @socketio.on('connect', namespace='/test')
    def connected():
        print('connected')
    #     TODO: show  wilson 1st question

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

    def user_save_login():
        u = Users()
        u.room_id = get_current_room_id()
        #  TODO: encryption
        u.encrypted_room_id = get_current_room_id()
        u.last_question_id = 0
        u.save()
        login_user(u, remember=True)

    def register_user():
        """
        save as new user
        :return:
        """
        user_save_login()
        print('test')
        return redirect(url_for('page.privacy'))


    def get_current_room_id():
        room_ids = rooms()
        room_id = get_first_item(room_ids)
        return room_id

    @socketio.on('user_answer_event', namespace='/test')
    def handle_user_answer_event(json_data, methods=['GET', 'POST']):
        room_id = get_current_room_id()
        msg = json_data['message']
        q_id = json_data['q_id']

        if q_id == 0:
            print('start register user')
            register_user()

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

    app.register_blueprint(page)
    app.register_blueprint(contact)
    # app.register_blueprint(user)
    app.register_blueprint(api)
    extensions(app)
    authentication(app, Users)

    if __name__ == '__main__':
        socketio.run(app, manage_ssesion=False)

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
    # login_manager.login_view = 'user.login'

    @login_manager.user_loader
    # def load_user(uid):
    def load_user(room_id):
        print('@login_manager.user_loader')
        # return user_model.query.get(room_id)
        return user_model.query.filter_by(room_id=room_id).first()


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
