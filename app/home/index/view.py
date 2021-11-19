from sys import stdout

from flask.globals import request
from app.home.vuln.models import Vuln
from app.home.http.models import Http
from app.home.subdomain.models import Subdomain
from flask import render_template
from app import db
from flask_login import current_user
import math
from subprocess import Popen, PIPE
from app.home.index.models import Indexmethod, Runlog
from app.home.index.forms import indexForm
from app.home import utils
import time

#首页
def indexview(DynamicModel = Indexmethod, DynamicFrom = indexForm):
    if(request.method == "POST"):
        tmp = request.form
        tmp = tmp.to_dict()
        tmp['index_time'] = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
        dic = utils.form_to_model(tmp, DynamicModel())
        dic = utils.model_to_dict_2(dic)
        dic['id'] = 1
        db.session.query(DynamicModel).update(dic)
        db.session.commit()

    #记事本
    DynamicFrom = indexForm()
    nownote = db.session.query(DynamicModel).first()
    nownote = utils.queryToDict(nownote)
    utils.dict_to_form(nownote, DynamicFrom)

    #日志
    runlog = db.session.query(Runlog).order_by(Runlog.id.desc()).limit(20).all() 
    runlog = utils.queryToDict(runlog)


    subdomain_total_count = db.session.query(Subdomain).count()
    subdomain_new_count = db.session.query(Subdomain).filter(Subdomain.subdomain_new == 0).count()
    subdomain_rate = format(subdomain_new_count / subdomain_total_count * 100, '.2f') if subdomain_total_count else 0

    http_total_count = db.session.query(Http).count()
    http_new_count = db.session.query(Http).filter(Http.http_new == 0).count()
    http_rate = format(http_new_count / http_total_count * 100, '.2f') if http_total_count else 0


    vuln_total_count = db.session.query(Vuln).count()
    vuln_new_count = db.session.query(Vuln).filter(Vuln.vuln_new == 0).count()
    vuln_rate = format(vuln_new_count / vuln_total_count * 100, '.2f') if vuln_total_count else 0

    #获取celery状态
    cmd = ["python3", '-m', 'celery', '-A', 'app.home.index.celery_status', 'inspect', 'active']
    p = Popen(cmd, shell=False, stdout = PIPE)
    celery_result = {}
    tmp = ""
    for line in iter(p.stdout.readline, b''):
        line = str(line)
        if(': OK\\n' in line):
            if tmp == "":
                tmp = line.split("@")[1].split("_")[0]
        else:
            if tmp not in celery_result:
                celery_result[tmp] = [0,0]
            if("empty -\\n" in line):
                celery_result[tmp][0] = celery_result[tmp][0] + 1
            elif('*' in line):
                celery_result[tmp][1] = celery_result[tmp][1] + 1
            else:
                pass
            tmp = ""
    p.stdout.close()
    try:
        del celery_result['']
    except:
        pass

    content = {'subdomain_total_count' : subdomain_total_count, 'subdomain_new_count': subdomain_new_count, 'subdomain_rate': subdomain_rate,
                'http_total_count': http_total_count, 'http_new_count': http_new_count, 'http_rate': http_rate,
                'vuln_total_count': vuln_total_count, 'vuln_new_count': vuln_new_count, 'vuln_rate': vuln_rate,
                'celery_result': celery_result,
                'runlog': runlog,
                }

    return render_template('index.html', form = content, segment='index', indexnote = DynamicFrom)