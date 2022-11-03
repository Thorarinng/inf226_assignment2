# Flask wtf and wtfforms modules imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# constants imports constants.py
from constants import MESSAGE_MIN_LENGTH, MESSAGE_MAX_LENGTH, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH

class MessageForm(FlaskForm):
    # receiver = username
    receiver = StringField('Receiver', validators=[DataRequired(),Length(min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH, message="Username length must be between %(min)d and %(max)dcharacters")])
    text = StringField('Msg',validators=[DataRequired(), Length(min=MESSAGE_MIN_LENGTH, max=MESSAGE_MAX_LENGTH, message="Message length must be between %(min)d and %(max)dcharacters")])
    submit = SubmitField('Submit')

