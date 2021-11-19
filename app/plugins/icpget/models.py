from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import LONGTEXT

from app import db

class plugins_icp(db.Model):
    __tablename__ = 'plugins_Icp'
    id = Column(Integer, autoincrement=True, primary_key=True)
    icp_cookie = Column(LONGTEXT)