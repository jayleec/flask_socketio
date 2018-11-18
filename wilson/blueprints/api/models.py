from flask import current_app
# from flask_login import utils
from datetime import datetime
import pytz
from lib.util_sqlalchemy import ResourceMixin
from wilson.extensions import db
from hashlib import md5
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash


class Users(ResourceMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='1')
    room_id = db.Column(db.String(200), unique=True, nullable=False, server_default='')
    encrypted_room_id = db.Column(db.String(3600), nullable=False, server_default='')
    # last answered question's number
    last_question_id = db.Column(db.Integer)

    # __tablename__ = 'users'

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        # self.encrypted_room_id = User.encrypt_password(kwargs.get('encrypted_room_id', ''))

    def __repr__(self):
        return '<Users {}>'.format(self.session_id)

    def get_id(self):
        print('get_id')
        # return self.room_id
        return self.room_id

    def is_authenticated(self, room_id):
        return room_id == self.room_id

    @classmethod
    def find_by_cookie_token(cls, token):
        return Users.query.filter(Users.cookie_token == token).first()

    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return generate_password_hash(plaintext_password)

        return None

    @classmethod
    def deserialize_token(cls, token):
        """
        Obtain a Users from de-serializing a signed token.

        :param token: Signed token.
        :type token: str
        :return: Users instance or None
        """
        private_key = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'])
        try:
            decoded_payload = private_key.loads(token)

            # return User.find_by_identity(decoded_payload.get('user_email'))
            return Users.find_by_cookie_token(decoded_payload.get('roorm_id'))
        except Exception:
            return None

    def is_active(self):
        """
        Return whether or not the user account is active, this satisfies
        Flask-Login by overwriting the default value.

        :return: bool
        """
        return self.active

    def get_auth_token(self):
        """
        Return the user's auth token. Use their password as part of the token
        because if the user changes their password we will want to invalidate
        all of their logins across devices. It is completely fine to use
        md5 here as nothing leaks.

        This satisfies Flask-Login by providing a means to create a token.

        :return: str
        """
        private_key = current_app.config['SECRET_KEY']

        serializer = URLSafeTimedSerializer(private_key)
        # data = [str(self.id), md5(self.password.encode('utf-8')).hexdigest()]
        data = [str(self.id), md5(self.encrypted_room_id.encode('utf-8')).hexdigest()]

        return serializer.dumps(data)

    def authenticated(self, with_password=True, password=''):
        print('authenticating')
        """
        Ensure a user is authenticated, and optionally check their password.

        :param with_password: Optionally check their password
        :type with_password: bool
        :param password: Optionally verify this as their password
        :type password: str
        :return: bool
        """
        if with_password:
            # return check_password_hash(self.password, password)
            return check_password_hash(self.encrypted_room_id, password)

        return True

    def serialize_token(self, expiration=3600):
        """
        Sign and create a token that can be used for things such as resetting
        a password or other tasks that involve a one off token.

        :param expiration: Seconds until it expires, defaults to 1 hour
        :type expiration: int
        :return: JSON
        """
        private_key = current_app.config['SECRET_KEY']

        serializer = TimedJSONWebSignatureSerializer(private_key, expiration)
        # return serializer.dumps({'user_email': self.email}).decode('utf-8')
        return serializer.dumps({'roorm_id': self.room_id}).decode('utf-8')

    def update_activity_tracking(self, current_quetion_id):
        """
        update
        """
        self.last_question_id = current_quetion_id
        return self.save()


class Reply(ResourceMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    question_id = db.Column(db.Integer)
    user_id = db.Column(db.String(128))
    feedback_id = db.Column(db.String(128))
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    message = db.Column(db.String(302))

    def __repr__(self):
        return '<Reply {}>'.format(self.user_id)


class Questions(ResourceMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    text = db.Column(db.String(1000))

    def __repr__(self):
        return '<Questions {}>'.format(self.id)


class Feedback(ResourceMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    question_id = db.Column(db.Integer)
    text = db.Column(db.String(2000))

    def __repr__(self):
        return '<Feedback {}>'.format(self.id)


class Report(ResourceMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    question_id = db.Column(db.Integer)
    text = db.Column(db.String(2000))

    def __repr__(self):
        return '<Report {}>'.format(self.id)
