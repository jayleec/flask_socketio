from flask_wtf import Form
from wtforms import HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length

class UserReplyForm(Form):
    question_id = HiddenField()
    user_id = HiddenField()
    feedback_id = HiddenField()
    message = TextAreaField("What's your answer?",
                            [DataRequired(), Length(1, 300)])
