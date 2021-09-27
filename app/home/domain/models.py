from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean

from app import db

# 域名信息管理
class Domain(db.Model):
    __tablename__ = 'Domain'
    id = Column(Integer, autoincrement=True, primary_key=True)
    domain_name = Column(String(128), unique=True)   #扫描域名名
    domain_user = Column(String(128))   #添加用户
    domain_time = Column(String(128))   #修改时间
    domain_target = Column(Integer) #隶属于的目标
