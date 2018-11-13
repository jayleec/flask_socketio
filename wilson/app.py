from threading import Lock
from flask import Flask, request

from flask_socketio import SocketIO, emit, join_room, leave_room, send, rooms
from flask_session import Session
from flask_login import LoginManager, UserMixin

from wilson.blueprints.page import page
from wilson.extensions import debug_toolbar


#  TODO: delete client_list
client_list = []

async_mode = "eventlet"
thread = None
thread_lock = Lock()
app = Flask(__name__, instance_relative_config=True)
socketio = SocketIO(app, async_mode=async_mode, manage_session=False)


CELERY_TASK_LIST = [
    'wilson.blueprints.contact.tasks',
]


def create_app(settings_override=None):
    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)
    app.config['SECRET_KEY'] = 'somthingsecret!'

    @socketio.on('connect', namespace='/test')
    def connected():
        print('connected')
    #     show  wilson 1st question

    def get_first_item(list):
        if list:
            return list[0]

    def messageReceived(methods=['GET', 'POST']):
        print('message was received!!!')

    @socketio.on('user_answer_event', namespace='/test')
    def handle_user_answer_event(json, methods=['GET', 'POST']):
        print('[user_answer_event] received my event json : ' + str(json))
        roomIds = rooms()
        print('[user_answer_event] all rooms : ', roomIds)
        roomId = get_first_item(roomIds)
        print("[user_answer_event] ", roomId)
        client_list.append(roomId)
        #  store  REPLY
        emit('my response', json['message'], callback=messageReceived, namespace='/test')

    def userJoined():
        print('[userJoined] new user joined')

    @socketio.on('join', namespace='/test')
    def on_join(data):
        username = data['username']
        # room = data['room']
        # join_room(room_id)
        print('[join] joined room number ' + str())
        # emit('join response', data, callback=userJoined, namespace='/test')
        # send(username + ' has entered the room.', room=room)

    @socketio.on('leave', namespace='/test')
    def on_leave(data):
        username = data['username']
        room = data['room']
        print('[leave] left room number ' + room)
        leave_room(room)
        send(username + ' has left the room.', room=room)

    login = LoginManager(app)
    Session(app)

    app.register_blueprint(page)

    if __name__ == '__main__':
        socketio.run(app)

    return app



def background_thread():
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)

    return None