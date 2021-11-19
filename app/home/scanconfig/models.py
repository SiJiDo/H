from app import db

# 扫描引擎模式
class Scanmethod(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'Scanmethod'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    scanmethod_name = db.Column(db.String(128))   #扫描方式名
    scanmethod_subfinder = db.Column(db.Boolean, default=False) #是否扫描subfinder
    scanmethod_amass = db.Column(db.Boolean, default=False) #是否扫描amass
    scanmethod_shuffledns = db.Column(db.Boolean, default=False) #是否扫描amass
    scanmethod_second = db.Column(db.Boolean, default=False) # 基于已有的子域名，对二级域名爆破
    scanmethod_port = db.Column(db.Boolean, default=False)  #是否扫描端口
    scanmethod_port_portlist = db.Column(db.String(128))  #扫描端口类型选择
    scanmethod_port_dfportlist = db.Column(db.String(255))  #自定义端口
    scanmethod_httpx = db.Column(db.Boolean, default=False) #是否扫描http
    scanmethod_ehole = db.Column(db.Boolean, default=False) #是否扫描指纹
    scanmethod_screenshot = db.Column(db.Boolean, default=False) #是否截图
    scanmethod_jsfinder = db.Column(db.Boolean, default=False) #是否扫描js中的路径
    scanmethod_dirb = db.Column(db.Boolean, default=False)   #是否扫描目录
    scanmethod_dirb_wordlist = db.Column(db.String(128))  #扫描字典选择
    scanmethod_xray = db.Column(db.Boolean, default=False)    #是否xray扫描漏洞
    scanmethod_nuclei = db.Column(db.Boolean, default=False)    #是否nuclei扫描漏洞
    scanmethod_nuclei_my = db.Column(db.Boolean, default=False)    #是否nuclei自定义脚本扫描漏洞
    scanmethod_time = db.Column(db.String(128))   #修改时间


# 定时引擎模式
class Scancron(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'Scancron'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    scancron_name = db.Column(db.String(20))   #定时名
    scancron_month = db.Column(db.String(20)) #定时月
    scancron_week = db.Column(db.String(20))  #定时周
    scancron_day = db.Column(db.String(20))  #定时天
    scancron_hour = db.Column(db.String(20)) #定时小时
    scancron_min = db.Column(db.String(20)) #定时分钟
    scancron_time = db.Column(db.String(20))   #修改时间

# 记录计划任务
class Cronjob(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'Cronjob'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cornjob_pid = db.Column(db.String(128))   #计划任务进程

