from app import db
from sqlalchemy.dialects.mysql import LONGTEXT

# 扫描引擎模式
class Indexmethod(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'Indexnote'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    index_note = db.Column(LONGTEXT)   # 笔记
    index_time = db.Column(db.String(128))   #修改时间

class Runlog(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'Runlog'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    log_info = db.Column(LONGTEXT)   # 日志
    log_time = db.Column(db.String(128))   #修改时间
