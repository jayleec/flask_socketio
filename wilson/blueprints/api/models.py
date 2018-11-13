from datetime import datetime
from wilson.extensions import db

class Reply(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    question_id = db.Column(db.String(128))
    user_id = db.Column(db.String(128))
    feedback_id = db.Column(db.String(128))
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    message = db.Column(db.String(2000))

    def __repr__(self):
        return '<Reply {}>'.format(self.user_id)