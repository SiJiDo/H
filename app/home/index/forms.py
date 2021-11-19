from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField,SubmitField,TextAreaField
from wtforms.validators import  DataRequired
import time

class indexForm(FlaskForm):
    index_note = TextAreaField('记事本',)
    submit = SubmitField('保存')