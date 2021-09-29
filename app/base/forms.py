# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,IntegerField
from wtforms.validators import InputRequired, Email, DataRequired

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password' , id='pwd_old'      , validators=[DataRequired()])
    newpassword1 = PasswordField('Password' , id='pwd_new1'      , validators=[DataRequired()])
    newpassword2 = PasswordField('Password' , id='pwd_new2'      , validators=[DataRequired()])