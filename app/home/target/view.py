from app.home.target.function import saveblacklist, savedomain, savesubdomain
from app.home.target.models import *
from app.home.utils import *
from flask import render_template, request
from app.home.scanconfig.models import *
from app import db
from app.home.target.form import *
from flask_login import current_user
import math
import time

#target目录总览
def target(DynamicModel = Target):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else 10
    query = ""
    search = ""
    total_count = ""


    #删除单个项目
    if(action == 'delete'):
        if(is_admin()):
            db.session.query(DynamicModel).filter(DynamicModel.id == id).delete()
        else:
            db.session.query(DynamicModel).filter(DynamicModel.id == id).filter(DynamicModel.target_user == str(current_user)).delete()
        db.session.commit()
        flash("删除成功")

    #删除多个项目
    if(action == 'deleteall'):
        print(request.args.to_dict())
        ids = []
        for i in request.args.to_dict():
            if(i == 'action' or i == 'page' or i == 'search'):
                continue
            ids.append(i)
        print(ids)
        for id in ids:
            if(is_admin()):
                db.session.query(DynamicModel).filter(DynamicModel.id == id).delete() 
            else:
                db.session.query(DynamicModel).filter(DynamicModel.id == id).filter(DynamicModel.target_user == str(current_user)).delete()
        db.session.commit()
        flash("删除成功")

    #查询
    search = request.args.get('search')
    print(search)
    if search != 'None' and search and '=' in search:
        target = ""
        start_time = "2021-01-01 00:00:00"
        end_time = "2099-01-01 00:00:00"
        user = ""
        info = search.split("&&")
        for i in info:
            if('target' in i):
                target = i.split("=")[1]
            if('start_time' in i):
                start_time = i.split("=")[1]
            if('end_time' in i):
                end_time = i.split("=")[1]
            if('user' in i):
                user = i.split("=")[1]
            print(i)

        search = search.replace("&&", "%26%26")
        if(is_admin()):
            query = DynamicModel.query.filter(
                    DynamicModel.target_name.like("%{}%".format(target)),
                    DynamicModel.target_time <= end_time, 
                    DynamicModel.target_time >= start_time,
                    DynamicModel.target_user.like("%{}%".format(user)),
                    ).order_by(DynamicModel.id.desc()).paginate(page, length)

            total_count = DynamicModel.query.filter(
                DynamicModel.target_name.like("%{}%".format(target)),
                DynamicModel.target_time <= end_time, 
                DynamicModel.target_time >= start_time,
                DynamicModel.target_user.like("%{}%".format(user)),
                ).count()
        else:
            query = DynamicModel.query.filter(
                    DynamicModel.target_name.like("%{}%".format(target)),
                    DynamicModel.target_time <= end_time, 
                    DynamicModel.target_time >= start_time,
                    DynamicModel.target_user.like("%{}%".format(user)),
                    DynamicModel.target_user == str(current_user),
                    ).order_by(DynamicModel.id.desc()).paginate(page, length)

            total_count = DynamicModel.query.filter(
                DynamicModel.target_name.like("%{}%".format(target)),
                DynamicModel.target_time <= end_time, 
                DynamicModel.target_time >= start_time,
                DynamicModel.target_user.like("%{}%".format(user)),
                DynamicModel.target_user == str(current_user),
                ).count()
    else:
        if(is_admin()):
            query = DynamicModel.query.order_by(DynamicModel.id).paginate(page, length)
            total_count = DynamicModel.query.count()
        else:
            query = DynamicModel.query.filter(DynamicModel.target_user == str(current_user)).order_by(DynamicModel.id).paginate(page, length)
            total_count = DynamicModel.query.filter(DynamicModel.target_user == str(current_user)).count()

    content = []
    #转换成dict
    for q in query.items:
        content.append(queryToDict(q))
    for i in content:
        i['domain_total_count'] = 0
        i['http_total_count'] = 0
    dict = {'content': content, 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length, 'search': search}
    return render_template('target.html',form = dict)

#target添加
def targetadd(DynamicModel = Target, form = TargetForm):
    form = TargetForm()
    #定义扫描模式下拉框
    model = Scanmethod.query.all()
    model = queryToDict(model)
    list = [(c['id'],c['scanmethod_name']) for c in model]
    form.target_method.choices = list

    #定义扫描周期下拉框
    model = Scancron.query.all()
    model = queryToDict(model)
    list_cron = [(c['id'],c['scancron_name']) for c in model]
    form.target_cron_id.choices = list_cron

    #处理发送添加请求
    if request.method == 'POST':
        print()
        tmpform = request.form.to_dict()
        target = form_to_model(tmpform, DynamicModel())
        
        #设置target的其他属性
        target.target_cron = True if  target.target_cron == "True" else False
        target.target_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
        target.target_status = 0
        target.target_user = str(current_user)
        target.target_pid = 0
        db.session.add(target)
        db.session.commit()
        #设置blacklist的其他属性
        saveblacklist(target.black_name, target.id)
        #设置domain的其他属性
        savedomain(target.domain_name, target.id, current_user)
        #设置subdomain的其他属性
        savesubdomain(target.subdomain_name, target.id, current_user)
        flash("添加成功")

    return render_template('targetadd.html', form=form)

#target详细
def targetinfo(DynamicModel = Target, DynamicFrom = TargetForm):
    DynamicFrom = TargetForm()
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    query = ""
    message = request.args.get('message')
    if(message):
        flash(message)

    if(is_admin()):
        query = DynamicModel.query.filter(DynamicModel.id == id).first()
    else:
        query = DynamicModel.query.filter(DynamicModel.id == id).filter(DynamicModel.target_user == str(current_user)).order_by(DynamicModel.id).first()
    dict = {'content': query, 
            }
    return render_template('targetinfo.html', form=dict, id=id)

#target修改
def targetedit(DynamicModel = Target, DynamicFrom = TargetForm):
    DynamicFrom = TargetForm()
    # 接收参数
    id = request.args.get('id')

    #定义扫描模式下拉框
    model = Scanmethod.query.all()
    model = queryToDict(model)
    list = [(c['id'],c['scanmethod_name']) for c in model]
    DynamicFrom.target_method.choices = list

    #定义扫描周期下拉框
    model = Scancron.query.all()
    model = queryToDict(model)
    list_cron = [(c['id'],c['scancron_name']) for c in model]
    DynamicFrom.target_cron_id.choices = list_cron
    
    count  = DynamicModel.query.filter(DynamicModel.target_user == str(current_user), DynamicModel.id == id).count()
    if(not is_admin() and count == 0 ):
        flash("该资产不是你添加的")
        return render_template('page-500.html')

    nowstarget = db.session.query(DynamicModel).filter(DynamicModel.id == id).first()
    nowstarget = queryToDict(nowstarget)
    dict_to_form(nowstarget, DynamicFrom)

    #处理发送添加请求
    if request.method == 'POST':
        print()
        tmpform = request.form.to_dict()
        target = form_to_model(tmpform, DynamicModel())
        
        #设置target的其他属性
        target.target_cron = True if  target.target_cron == "True" else False
        target.target_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
        target.target_status = 0
        target.target_user = str(current_user)
        target.target_pid = 0
        target.id = id
        dic = model_to_dict_2(target)
        db.session.query(DynamicModel).filter(DynamicModel.id == id).update(dic)
        db.session.commit()
        #设置blacklist的其他属性
        saveblacklist(target.black_name, target.id)
        #设置domain的其他属性
        savedomain(target.domain_name, target.id, current_user)
        #设置subdomain的其他属性
        savesubdomain(target.subdomain_name, target.id, current_user)
        flash("修改成功")

    return render_template('targetedit.html', form=DynamicFrom, id=id)