from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
import time

class IcpForm(FlaskForm):
    icp_cookie = StringField('cookie')

    submit = SubmitField('修改')


