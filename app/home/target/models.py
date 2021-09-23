from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean

from app import db


class Target(db.Model):
    __tablename__ = 'Target'
    id = Column(Integer, autoincrement=True, primary_key=True)
    target_name = Column(String(128))   #扫描目标名
    target_description = Column(String(128))    #扫描目标描述
    target_method = Column(String(128))  #扫描方式的引擎
    target_cron = Column(Boolean, default=False)   #是否周期扫描
    target_cron_id = Column(String(128))    #周期扫描的引擎
    target_status = Column(Integer, default=0)   #扫描0表示未扫描，1表示扫描中，2表示扫完完成
    target_user = Column(String(128))   #扫描0表示未扫描，1表示扫描中，2表示扫完完成
    target_pid = Column(Integer, default=0) #扫描进程
    target_time = Column(String(128))   #修改时间

class Blacklist(db.Model):
    __tablename__ = 'Blacklist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    black_name = Column(String(128), unique=True)   #黑名单内容，以domain,ip,title三类标志
    black_time = Column(String(128))   #修改时间
    black_target = Column(Integer) #隶属于的目标
