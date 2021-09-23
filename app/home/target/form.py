from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
import time

class TargetForm(FlaskForm):
    target_name = StringField('目标名', validators=[DataRequired(message='不能为空')])
    target_description = TextAreaField('目标描述', validators=[DataRequired(message='不能为空')])
    target_time = StringField('目标修改时间', default=time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())))
    target_method = SelectField('扫描模式名')
    target_cron = SelectField('周期监控', choices=[(True, '是'), (False, '否')])
    target_cron_id = SelectField('扫描周期名')
    target_status = IntegerField('扫描状况', default=0)
    black_name = TextAreaField('黑名单添加')
    domain_name = TextAreaField('主域名资产添加')
    subdomain_name = TextAreaField('精准域名资产添加')

    submit = SubmitField('添加/修改')


