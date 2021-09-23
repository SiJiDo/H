# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField,SubmitField,SelectField
from wtforms.validators import  DataRequired
import time

#对年月日进行预设
list_min = []
for i in range(0, 60):
    list_min.append((str(i),str(i)))
list_hour = [('*','*')]
for i in range(0,24):
    list_hour.append((str(i),str(i)))
list_day = [('*','*')]
for i in range(1,32):
    list_day.append((str(i),str(i)))

list_day_of_week = [('*','*')]
for i in range(1,8):
    list_day_of_week.append((str(i),str(i)))

list_month = [('*','*')]
for i in range(1,13):
    list_month.append((str(i),str(i)))

class ScanmethodForm(FlaskForm):
    scanmethod_name = StringField('扫描模式名', validators=[DataRequired(message='不能为空')])
    scanmethod_subfinder = BooleanField('subfinder扫描',default=False)
    scanmethod_amass = BooleanField('amass扫描',default=False)
    scanmethod_shuffledns = BooleanField('shuffledns扫描',default=False)
    scanmethod_github = BooleanField('github扫描',default=False)
    scanmethod_port = BooleanField('端口扫描',default=False)
    scanmethod_port_portlist = SelectField('端口模式', choices=[('top100', 'top100端口'), ('top1000', 'top1000端口'),('all', '全端口'),('deafult', '自定义')])
    scanmethod_port_dfportlist = StringField('自定义端口',)
    scanmethod_httpx = BooleanField('站点扫描',default=False)
    scanmethod_ehole = BooleanField('站点指纹识别',default=False)
    scanmethod_screenshot = BooleanField('站点截图',default=False)
    scanmethod_jsfinder = BooleanField('站点扫描',default=False)
    scanmethod_dirb = BooleanField('目录扫描',default=False)
    scanmethod_dirb_wordlist =  SelectField('目录字典', choices=[('top100', 'top100字典'),('top1000', 'top1000字典'), ('top7000', 'top7000字典')])
    scanmethod_xray = BooleanField('rad+xray扫描',default=False)
    scanmethod_nuclei = BooleanField('nuclei扫描',default=False)
    scanmethod_nuclei_my = BooleanField('nuclei(自定义扫描)',default=False)
    scanmethod_time = StringField('目标修改时间', default=time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())))
    submit = SubmitField('创建')

class ScancronFrom(FlaskForm):
    scancron_name = StringField('定时器名', validators=[DataRequired(message='不能为空')])   #定时名
    scancron_month = SelectField('月', choices=list_month) #定时月
    scancron_week = SelectField('周', choices=list_day_of_week)  #定时周
    scancron_day = SelectField('日', choices=list_day)  #定时天
    scancron_hour = SelectField('小时', choices=list_hour) #定时小时
    scancron_min = SelectField('分钟', choices=list_min) #定时分钟
    scancron_time = StringField('目标修改时间', default=time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())))   #修改时间
    submit = SubmitField('提交')


