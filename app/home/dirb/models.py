from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.dialects.mysql import LONGTEXT

from app import db

# 目录信息管理
class Dirb(db.Model):
    __tablename__ = 'Dirb'
    id = Column(Integer, autoincrement=True, primary_key=True)
    dir_base = Column(String(128), unique=True)   # url路径
    dir_path = Column(String(128))   # 路径
    dir_status = Column(String(128))   # dirb 响应码
    dir_length = Column(String(128)) # dirb 响应长度
    dir_title = Column(String(128)) # dirb 目录名
    dir_time = Column(String(128))   # 修改时间
    dir_http = Column(Integer) # 隶属于的http
    dir_tool = Column(String(128)) # 通过何种工具收集
    dir_user = Column(String(128)) # 添加用户
    dir_new = Column(String(128)) # 是否为新增
    dir_target = Column(Integer) # 隶属于的目标