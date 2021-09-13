from app import db

# 扫描引擎模式
class scanmethod(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'hhsrc_scanmethod'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    scanmethod_name = db.Column(db.String(128))   #扫描方式名
    scanmethod_subdomain = db.Column(db.Boolean, default=True) #是否扫描子域名
    scanmethod_port = db.Column(db.Boolean, default=True)  #是否扫描端口
    scanmethod_port_portlist = db.Column(db.String(128))  #扫描端口类型选择
    scanmethod_url = db.Column(db.Boolean, default=True) #是否扫描http
    scanmethod_dirb = db.Column(db.Boolean, default=False)   #是否扫描目录
    scanmethod_dirb_wordlist = db.Column(db.String(128))  #扫描字典选择
    scanmethod_vuln = db.Column(db.Boolean, default=False)    #是否扫描指纹
    scanmethod_time = db.Column(db.String(128))   #修改时间

# 定时引擎模式
class scancorn(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'hhsrc_scancorn'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    scancorn_name = db.Column(db.String(20))   #定时名
    scancorn_month = db.Column(db.String(20)) #定时月
    scancorn_week = db.Column(db.String(20))  #定时周
    scancorn_day = db.Column(db.String(20))  #定时天
    scancorn_hour = db.Column(db.String(20)) #定时小时
    scancorn_min = db.Column(db.String(20)) #定时分钟
    scancorn_time = db.Column(db.String(20))   #修改时间

# 记录计划任务
class cornjob(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'hhsrc_cornjob'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cornjob_name = db.Column(db.String(128))  #计划任务名字
    cornjob_time = db.Column(db.String(128))  #计划任务时间