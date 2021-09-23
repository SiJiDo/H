from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean

from app import db

# port信息管理
class Port(db.Model):
    __tablename__ = 'Port'
    id = Column(Integer, autoincrement=True, primary_key=True)
    port_domain = Column(String(128))   #ip对应域名
    port_ip = Column(String(128))   #ip域名
    port_port = Column(String(128))   #ip端口
    port_server = Column(String(128))   #ip服务
    port_http_status = Column(Boolean, default=False)   #http扫描状态
    port_time = Column(String(128))   #修改时间
    port_user = Column(String(128)) # 添加用户
    port_new = Column(Integer) #是否是新增
    port_target = Column(Integer) #隶属于的目标