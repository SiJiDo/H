import configparser
import pymysql

cfg = configparser.ConfigParser()
cfg.read('config.ini')

def dbconn():
    #初始化数据库连接
    DB_HOST = cfg.get("DATABASE", "DB_HOST")
    DB_USER = cfg.get("DATABASE", "DB_USER")
    DB_PORT = cfg.get("DATABASE","DB_PORT")
    DB_PASSWD = cfg.get("DATABASE", "DB_PASSWD")
    DB_DATABASE = cfg.get("DATABASE", "DB_DATABASE")
    conn = pymysql.connect(host=DB_HOST, port=int(DB_PORT), user=DB_USER, password=DB_PASSWD, db=DB_DATABASE, charset='utf8')
    cursor = conn.cursor()
    return conn,cursor