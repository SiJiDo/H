from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
import time

class HostcrackForm(FlaskForm):
    hostcrack_domain = TextAreaField('碰撞域名')
    hostcrack_ip = TextAreaField('碰撞ip')
    hostcrack_result = TextAreaField('碰撞结果')
    hostcrack_time = StringField('碰撞时间', default=time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())))

    submit = SubmitField('开始碰撞')


