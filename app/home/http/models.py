from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.dialects.mysql import LONGTEXT

from app import db

# http信息管理
class Http(db.Model):
    __tablename__ = 'Http'
    id = Column(Integer, autoincrement=True, primary_key=True)
    http_schema = Column(String(128)) #协议
    http_name = Column(String(128), unique=True)   # url信息
    http_title = Column(String(128))   #http 标题
    http_status = Column(String(128))   # http 响应码
    http_length = Column(String(128))   # http 响应长度
    http_screen = Column(LONGTEXT)   # http 页面截图
    http_finger = Column(String(128))   # http 指纹
    http_see = Column(Boolean, default=False) #是否已读
    http_new = Column(Integer) #是否是新增
    http_time = Column(String(128))   #修改时间
    http_user = Column(String(128))   # 扫描用户
    http_target = Column(Integer) #隶属于的目标