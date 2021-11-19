from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField, PasswordField
from wtforms.validators import DataRequired
import time

list_hour = []
for i in range(0,24):
    list_hour.append((str(i),str(i)+":00"))

class SysconfigForm(FlaskForm):
    config_email_username = StringField('邮箱账号') # 邮箱账号
    config_email_password = PasswordField('邮箱密码') # 邮箱密码
    config_email_server = StringField('邮箱服务器地址') # 邮箱域名
    config_email_get = TextAreaField('接收推送邮箱') # 接收推送邮箱
    config_push_hour = SelectField('每日推送时间', choices=list_hour)
    config_info = BooleanField('每日资产推送',default=False)   #是否发送今日新域名
    config_vuln = BooleanField('漏洞实时nuclei推送',default=False)   #是否发送实时漏洞
    config_vuln_github = StringField('自定义poc的github地址') # 自定义poc地址
    config_count = StringField('同时扫描任务上限设置', validators=[DataRequired(message='不能为空')]) # 最多几个任务同时扫描
    config_xray =  BooleanField('漏洞实时rad+xray漏洞推送',default=False)   #是否发送实时rad+xray漏洞
    config_vuln_my =  BooleanField('漏洞实时自定义漏洞推送',default=False)   #是否发送实时自定义漏洞
    config_nuclei_day =  BooleanField('漏洞每日新poc扫描',default=False)   #是否每日扫新poc

    submit = SubmitField('修改')


