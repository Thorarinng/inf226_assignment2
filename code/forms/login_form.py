# Flask wtf and wtf module
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Length

# Constants
from constants import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH, message="Username length must be between %(min)d and %(max)dcharacters")])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=PASSWORD_MIN_LENGTH, max=PASSWORD_MAX_LENGTH, message="Password length must be between %(min)d and %(max)dcharacters")])
    submit = SubmitField('Submit')

