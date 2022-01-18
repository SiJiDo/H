from app.home.scanconfig.models import *
from app.home.scanconfig.forms import *
from app.home.utils import * 
from app.home import utils
from flask import render_template,request,redirect,url_for
from app import db
import time

#扫描模式
def scanmethod(DynamicModel = Scanmethod, DynamicFrom = ScanmethodForm):
    DynamicFrom = ScanmethodForm()
    id = ""
    if(request.args.get('id')):
        id = int(request.args.get('id'))
    
    #新加
    if request.method == 'POST':
        tmpform = request.form
        tmpform = tmpform.to_dict()
        for i in tmpform:
           if tmpform[i] == 'y':
               tmpform[i] = True
        scanmethod = utils.form_to_model(tmpform, DynamicModel())
        scanmethod.scanmethod_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
        if(id):
            if('delete' in tmpform):
                db.session.query(DynamicModel).filter(DynamicModel.id == id).delete()
            elif('change' in tmpform):
                dic = utils.model_to_dict_2(scanmethod)
                for d in dic:
                    if dic[d] == None:
                        dic[d] = False
                dic['id'] = id
                db.session.query(DynamicModel).filter(DynamicModel.id == id).update(dic)
        else:
            db.session.add(scanmethod)
        db.session.commit()
        return redirect(url_for('home_blueprint.scanmethodroute'))
    
    #查看
    result = db.session.query(DynamicModel).all()
    flag = False
    if(id):
        nowscanmethod = db.session.query(DynamicModel).filter(DynamicModel.id == id).first()
        nowscanmethod = utils.queryToDict(nowscanmethod)
        utils.dict_to_form(nowscanmethod, DynamicFrom)
        flag = True
    if(result):
        dict = {'content': utils.queryToDict(result)}
    else:
        dict = {'content':{}}
    return render_template('scanmethod.html',form=DynamicFrom, dict = dict, id = id, flag=flag,segment=get_segment(request))


#扫描周期
def scancron(DynamicModel = Scancron, DynamicFrom = ScancronFrom):
    DynamicFrom = ScancronFrom()
    id = ""
    if(request.args.get('id')):
        id = int(request.args.get('id'))
    
    #新加
    if request.method == 'POST':
        tmpform = request.form.to_dict()
        scancron = utils.form_to_model(tmpform, DynamicModel())
        if(id):
            if('delete' in tmpform):
                db.session.query(DynamicModel).filter(DynamicModel.id == id).delete()
            elif('change' in tmpform):
                dic = utils.model_to_dict_2(scancron)
                for d in dic:
                    if dic[d] == None:
                        dic[d] = False
                dic['id'] = id
                db.session.query(DynamicModel).filter(DynamicModel.id == id).update(dic)
        else:
            db.session.add(scancron)
        db.session.commit()
        return redirect(url_for('home_blueprint.scancronroute'))
    
    #查看
    result = db.session.query(DynamicModel).all()
    flag = False
    if(id):
        nowscanmethod = db.session.query(DynamicModel).filter(DynamicModel.id == id).first()
        nowscanmethod = utils.queryToDict(nowscanmethod)
        utils.dict_to_form(nowscanmethod, DynamicFrom)
        flag = True
    if(result):
        dict = {'content': utils.queryToDict(result)}
    else:
        dict = {'content':{}}
    return render_template('scancron.html',form=DynamicFrom, dict = dict, id = id, flag=flag,segment=get_segment(request))