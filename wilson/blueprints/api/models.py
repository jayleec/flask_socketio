from datetime import datetime
from lib.util_sqlalchemy import ResourceMixin
from wilson.extensions import db


class User(ResourceMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    session_id = db.Column(db.String(128))
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.session_id)


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
        return '<Feedback {}>'.format(self.id)


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
        return '<Feedback {}>'.format(self.id)
