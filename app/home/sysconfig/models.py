from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.dialects.mysql import LONGTEXT

from app import db

# 通用配置
class Sysconfig(db.Model):
    __tablename__ = 'Sysconfig'
    id = Column(Integer, autoincrement=True, primary_key=True)
    config_email_username = Column(String(128)) # 邮箱账号
    config_email_password = Column(String(128)) # 邮箱密码
    config_email_server = Column(String(128)) # 邮箱域名
    config_email_get = Column(LONGTEXT)   # 推送目标邮箱
    config_info = Column(Boolean, default=False)   #是否发送今日新域名
    config_vuln = Column(Boolean, default=False)   #是否发送实时漏洞
    config_vuln_github = Column(String(128)) # 自定义poc地址
    config_count = Column(Integer,default=1) # 最多几个任务同时扫描
    config_push_hour = Column(String(128)) # 每日推送时间
    config_xray =  Column(Boolean, default=False)   #是否发送实时rad+xray漏洞
    config_vuln_my =  Column(Boolean, default=False)   #是否发送实时自定义漏洞
    config_nuclei_day = Column(Boolean, default=False)   #是否每日扫描新的nuclei漏洞
    