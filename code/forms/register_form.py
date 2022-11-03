# Flask imports 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Length

from constants import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH, message="Username length must be between %(min)d and %(max)dcharacters")])
    password1 = PasswordField('Password1', validators=[DataRequired(),Length(min=PASSWORD_MIN_LENGTH, max=PASSWORD_MAX_LENGTH, message="Password length must be between %(min)d and %(max)dcharacters")])
    password2 = PasswordField('Password2', validators=[DataRequired(),Length(min=PASSWORD_MIN_LENGTH, max=PASSWORD_MAX_LENGTH, message="Password length must be between %(min)d and %(max)dcharacters")])
    submit = SubmitField('Submit')

