from app.home.sysconfig.models import *
from app.home.sysconfig.forms import *
from app.home.utils import * 
from app.home import utils
from flask import render_template,request
from app import db
from app.schedulertasks.controller import restart_scheduler

import time

def sysconfig(DynamicModel = Sysconfig, DynamicFrom = SysconfigForm):
    DynamicFrom = SysconfigForm()
    nowscanmethod = db.session.query(DynamicModel).filter(DynamicModel.id == 1).first()
    nowscanmethod = utils.queryToDict(nowscanmethod)
    utils.dict_to_form(nowscanmethod, DynamicFrom)
    if request.method == 'POST':
        tmpform = request.form
        tmpform = tmpform.to_dict()
        for i in tmpform:
            if tmpform[i] == 'y':
                tmpform[i] = True
        sysconfig = utils.form_to_model(tmpform, DynamicModel())
        dic = utils.model_to_dict_2(sysconfig)
        for d in dic:
            if dic[d] == None:
                dic[d] = False
        if dic['config_email_password'] == '':
            dic['config_email_password'] = db.session.query(DynamicModel.config_email_password).filter(DynamicModel.id == 1).first().config_email_password
        dic['id'] = 1
        db.session.query(DynamicModel).filter(DynamicModel.id == 1).update(dic)
        #db.session.add(sysconfig)
        db.session.commit()
        #重新配置定时
        restart_scheduler()


    return render_template('sysconfig.html',form=DynamicFrom, segment=get_segment(request))