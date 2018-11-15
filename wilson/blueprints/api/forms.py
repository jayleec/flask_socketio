from flask_wtf import Form
from lib.util_wtforms import ModelForm
from wtforms import HiddenField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length

class UserReplyForm(ModelForm):
    # id = HiddenField()
    # question_id = HiddenField()
    # user_id = HiddenField()
    # feedback_id = HiddenField()
    # created_date = HiddenField()
    # message = TextAreaField("What's your answer?",
    #                         [DataRequired(), Length(1, 300)])
    # message = TextAreaField(validators=[
    #                         DataRequired(),
    #                         Length(1, 300)])
    next = HiddenField()
    message = StringField(validators=[DataRequired(),
                            Length(1, 16)])







