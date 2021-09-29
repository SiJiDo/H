from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.dialects.mysql import LONGTEXT

from app import db


class Vuln(db.Model):
    __tablename__ = 'Vuln'
    id = Column(Integer, autoincrement=True, primary_key=True)
    vuln_mainkey = Column(String(128), unique=True) #主键
    vuln_name = Column(String(128)) #漏洞名
    vuln_info = Column(String(128)) #漏洞信息
    vuln_level = Column(String(128)) #漏洞级别
    vuln_poc = Column(LONGTEXT) #漏洞路径
    vuln_http = Column(String(128)) #隶属于的http
    vuln_target = Column(Integer) #隶属于的目标
    vuln_user = Column(String(128)) #添加用户
    vuln_new = Column(Integer) #是否是新增
    vuln_tool = Column(String(128)) #收集工具
    vuln_time = Column(String(128)) # 修改时间