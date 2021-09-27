# 子域名信息管理
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean

from app import db

class Subdomain(db.Model):
    __tablename__ = 'Subdomain'
    id = Column(Integer, autoincrement=True, primary_key=True)
    subdomain_name = Column(String(128), unique=True)   #子域名
    subdomain_ip = Column(String(128))   #子域ip
    subdomain_info = Column(String(128))   #子域解析信息
    subdomain_tool = Column(String(128))   #通过何种工具收集到的
    subdomain_user = Column(String(128))   #添加用户
    subdomain_new = Column(Integer) #是否是新增
    subdomain_time = Column(String(128))   #修改时间
    subdomain_target = Column(Integer) #隶属于的目标