from flask import render_template
from flask.globals import request
import os
import time
from subprocess import Popen

from sqlalchemy.sql.operators import op

from app.home import utils
from app.home.target.function import *
from app.plugins.icpget.forms import IcpForm
from app.plugins.icpget.models import plugins_icp
from app.scan.conn import dbconn
from multiprocessing import Process
from celery import Celery

import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')


FILEPATH = os.path.split(os.path.realpath(__file__))[0]

def icpget(DynamicModel = plugins_icp, DynamicFrom = IcpForm):

    task = Celery(broker=cfg.get("CELERY_CONFIG", "CELERY_BROKER_URL"), backend=cfg.get("CELERY_CONFIG", "CELERY_RESULT_BACKEND"))
    task.conf.update(CELERY_TASK_SERIALIZER = 'json',CELERY_RESULT_SERIALIZER = 'json',CELERY_ACCEPT_CONTENT=['json'],CELERY_TIMEZONE = 'Asia/Shanghai',CELERY_ENABLE_UTC = False,)


    DynamicFrom = IcpForm()
    query = db.session.query(DynamicModel).first()
    nowcookie = utils.queryToDict(query)
    utils.dict_to_form(nowcookie, DynamicFrom)
    content = []
    allresult = []
    allresultkillsame = set()

    if(request.method == 'POST'):
        if(request.args.get("action") == 'setcookie'):
            cookie = request.form['icp_cookie']
            db.session.query(DynamicModel).update({'icp_cookie':cookie})
            db.session.commit()
            query = db.session.query(DynamicModel).first()
            nowcookie = utils.queryToDict(query)
            utils.dict_to_form(nowcookie, DynamicFrom)

        if(request.args.get("action") == 'geticp'):
            company = request.form['company']
            cookie = query.icp_cookie

            #调用celery
            icp_scan = task.send_task('icpget.run', args=(company,"auth_token="+cookie, ), queue='icpget')
            while True:
                if icp_scan.successful():
                    try:
                        content, allresult = icp_scan.result
                        break
                    except Exception as e:
                        print(e)
                        break
    for i in allresult:
        allresultkillsame.add(i[1])

    return render_template('icpget.html', segment='icp',form=DynamicFrom, content = content, allresult = allresult, allresultkillsame = allresultkillsame)