from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.dialects.mysql import LONGTEXT

from app import db

class plugins_Hostcrack(db.Model):
    __tablename__ = 'plugins_Hostcrack'
    id = Column(Integer, autoincrement=True, primary_key=True)
    hostcrack_domain = Column(LONGTEXT)
    hostcrack_ip = Column(LONGTEXT)
    hostcrack_result = Column(LONGTEXT)
    hostcrack_pid = Column(String(128))
    hostcrack_time = Column(String(128))
