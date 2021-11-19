from app.home.subdomain.models import Subdomain
from app.home.domain.models import Domain
from app.home.port.models import Port
from app.home.http.models import Http
from app.home.dirb.models import Dirb
from app.home.vuln.models import Vuln
from app.home.target.function import ip_addr, saveblacklist, savedomain, savesubdomain, output_excel
from app.home.target.models import *
from app.home.utils import *
from flask import render_template, request, send_from_directory
from app.home.scanconfig.models import *
from app import db
from app.home.target.form import *
from flask_login import current_user
from app.schedulertasks.controller import restart_scheduler
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
            result = DynamicModel.query.filter(DynamicModel.id == id).all()
            [db.session.delete(r) for r in result]
            result = Blacklist.query.filter(Blacklist.black_target == id).all()
            [db.session.delete(r) for r in result]
            result = Domain.query.filter(Domain.domain_target == id).all()
            [db.session.delete(r) for r in result]
            result = Subdomain.query.filter(Subdomain.subdomain_target == id).all()
            [db.session.delete(r) for r in result]
            result = Port.query.filter(Port.port_target == id).all()
            [db.session.delete(r) for r in result]
            result = Http.query.filter(Http.http_target == id).all()
            [db.session.delete(r) for r in result]
            result = Dirb.query.filter(Dirb.dir_target == id).all()
            [db.session.delete(r) for r in result]
            result = Vuln.query.filter(Vuln.vuln_target == id).all()
            [db.session.delete(r) for r in result]
        else:
            db.session.query(DynamicModel).filter(DynamicModel.id == id).filter(DynamicModel.target_user == str(current_user)).delete()
            result = DynamicModel.query.filter(DynamicModel.id == id).filter(DynamicModel.target_user == str(current_user)).all()
            [db.session.delete(r) for r in result]
            result = Blacklist.query.filter(Blacklist.black_target == id).filter(DynamicModel.target_user == str(current_user)).all()
            [db.session.delete(r) for r in result]
            result = Domain.query.filter(Domain.domain_target == id).filter(DynamicModel.target_user == str(current_user)).all()
            [db.session.delete(r) for r in result]
            result = Subdomain.query.filter(Subdomain.subdomain_target == id).filter(DynamicModel.target_user == str(current_user)).all()
            [db.session.delete(r) for r in result]
            result = Port.query.filter(Port.port_target == id).filter(DynamicModel.target_user == str(current_user)).all()
            [db.session.delete(r) for r in result]
            result = Http.query.filter(Http.http_target == id).filter(DynamicModel.target_user == str(current_user)).all()
            [db.session.delete(r) for r in result]
            result = Dirb.query.filter(Dirb.dir_target == id).filter(DynamicModel.target_user == str(current_user)).all()
            [db.session.delete(r) for r in result]
            result = Vuln.query.filter(Vuln.vuln_target == id).filter(DynamicModel.target_user == str(current_user)).all()
            [db.session.delete(r) for r in result]
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
                result = DynamicModel.query.filter(DynamicModel.id == id).all()
                [db.session.delete(r) for r in result]
                result = Blacklist.query.filter(Blacklist.black_target == id).all()
                [db.session.delete(r) for r in result]
                result = Domain.query.filter(Domain.domain_target == id).all()
                [db.session.delete(r) for r in result]
                result = Subdomain.query.filter(Subdomain.subdomain_target == id).all()
                [db.session.delete(r) for r in result]
                result = Port.query.filter(Port.port_target == id).all()
                [db.session.delete(r) for r in result]
                result = Http.query.filter(Http.http_target == id).all()
                [db.session.delete(r) for r in result]
                result = Dirb.query.filter(Dirb.dir_target == id).all()
                [db.session.delete(r) for r in result]
                result = Vuln.query.filter(Vuln.vuln_target == id).all()
                [db.session.delete(r) for r in result]
                
            else:
                db.session.query(DynamicModel).filter(DynamicModel.id == id).filter(DynamicModel.target_user == str(current_user)).delete()
                result = DynamicModel.query.filter(DynamicModel.id == id).filter(DynamicModel.target_user == str(current_user)).all()
                [db.session.delete(r) for r in result]
                result = Blacklist.query.filter(Blacklist.black_target == id).filter(DynamicModel.target_user == str(current_user)).all()
                [db.session.delete(r) for r in result]
                result = Domain.query.filter(Domain.domain_target == id).filter(DynamicModel.target_user == str(current_user)).all()
                [db.session.delete(r) for r in result]
                result = Subdomain.query.filter(Subdomain.subdomain_target == id).filter(DynamicModel.target_user == str(current_user)).all()
                [db.session.delete(r) for r in result]
                result = Port.query.filter(Port.port_target == id).filter(DynamicModel.target_user == str(current_user)).all()
                [db.session.delete(r) for r in result]
                result = Http.query.filter(Http.http_target == id).filter(DynamicModel.target_user == str(current_user)).all()
                [db.session.delete(r) for r in result]
                result = Dirb.query.filter(Dirb.dir_target == id).filter(DynamicModel.target_user == str(current_user)).all()
                [db.session.delete(r) for r in result]
                result = Vuln.query.filter(Vuln.vuln_target == id).filter(DynamicModel.target_user == str(current_user)).all()
                [db.session.delete(r) for r in result]
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
        if(i['target_status'] == 0):
            i['target_status_info'] = '未扫描'
        if(i['target_status'] == 1):
            i['target_status_info'] = '准备扫描'
        if(i['target_status'] == 2):
            i['target_status_info'] = '扫描子域名'
        if(i['target_status'] == 3):
            i['target_status_info'] = '扫描端口'
        if(i['target_status'] == 4):
            i['target_status_info'] = '扫描站点'
        if(i['target_status'] == 5):
            i['target_status_info'] = '扫描路径'
        if(i['target_status'] == 6):
            i['target_status_info'] = '扫描漏洞'
        if(i['target_status'] == 7):
            i['target_status_info'] = '扫描完成'

        i['domain_total_count'] = 0
        i['http_total_count'] = 0
    dict = {'content': content, 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length, 'search': search}
    return render_template('target.html',form = dict,segment=get_segment(request))

#target添加
def targetadd(DynamicModel = Target, form = TargetForm):
    form = TargetForm()

    #定义扫描模式下拉框
    if(Scanmethod.query.count()):
        model = Scanmethod.query.all()
        model = queryToDict(model)
        list = [(c['id'],c['scanmethod_name']) for c in model]
    else:
        list = []
    form.target_method.choices = list

    #定义扫描周期下拉框
    if(Scancron.query.count()):
        model = Scancron.query.all()
        model = queryToDict(model)
        list_cron = [(c['id'],c['scancron_name']) for c in model]
    else:
        list_cron = []
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

        #重新配置定时
        restart_scheduler()

        flash("添加成功")

    return render_template('targetadd.html', form=form, segment=get_segment(request))

#target详细
def targetinfo(DynamicModel = Target, DynamicFrom = TargetForm):
    DynamicFrom = TargetForm()
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    Blacklist_page = int(request.args.get('blacklist_page')) if request.args.get('blacklist_page') else 1
    Blacklist_length = int(request.args.get('blacklist_length')) if request.args.get('blacklist_length') else 6
    Domain_page = int(request.args.get('domain_page')) if request.args.get('domain_page') else 1
    Domain_length = int(request.args.get('domain_length')) if request.args.get('domain_length') else 6
    query = ""
    black = request.args.get('black')
    message = request.args.get('message')

    remove_id =  int(request.args.get('target_id')) if request.args.get('target_id') else 0 
    action = request.args.get('action') 
    if(action == 'delete_domain'):
        target_id = id
        b = Domain.query.filter(Domain.id == remove_id).first()
        b = b.domain_name
        result = Domain.query.filter(Domain.id == remove_id).all()
        [db.session.delete(r) for r in result]
        result = Subdomain.query.filter(Subdomain.subdomain_name.like("%.{}".format(b)), Subdomain.subdomain_target == target_id).all()
        [db.session.delete(r) for r in result]
        result = Port.query.filter(Port.port_domain.like("%.{}".format(b)), Port.port_target == target_id).all()
        [db.session.delete(r) for r in result]
        result = Http.query.filter(Http.http_name.like("%.{}".format(b)), Http.http_target == target_id).all()
        [db.session.delete(r) for r in result]
        result = Dirb.query.filter(Dirb.dir_base.like("%.{}%".format(b)), Dirb.dir_target == target_id).all()
        [db.session.delete(r) for r in result]
        result = Vuln.query.filter(Vuln.vuln_name.like("%.{}%".format(b)), Vuln.vuln_target == target_id).all()
        [db.session.delete(r) for r in result]
        db.session.commit()
        
    if(action == 'delete_blacklist'):
        result = Blacklist.query.filter(Blacklist.id == remove_id).all()
        [db.session.delete(r) for r in result]
        db.session.commit()

    if(message):
        flash(message)

    #获取blacklist的信息
    query_blacklist = Blacklist.query.filter(Blacklist.black_target == id,).paginate(Blacklist_page, Blacklist_length)
    blacklist_total_count = Blacklist.query.filter(Blacklist.black_target == id).count()

    if(is_admin):
        query = DynamicModel.query.filter(DynamicModel.id == id).first()
        # 获取domain的信息
        query_domain = Domain.query.filter(Domain.domain_target == id,).order_by(Domain.domain_time.desc(),Domain.id.desc()).paginate(Domain_page, Domain_length)
        domain_total_count = Domain.query.filter(Domain.domain_target == id).count()

    else:
        query = DynamicModel.query.filter(DynamicModel.id == id).filter(DynamicModel.target_user == str(current_user)).order_by(DynamicModel.id).first()
        # 获取domain的信息
        query_domain = Domain.query.filter(Domain.domain_target == id, Domain.Domain_use == str(current_user)).order_by(Domain.domain_time.desc(),Domain.id.desc()).paginate(Domain_page, Domain_length)
        domain_total_count = Domain.query.filter(Domain.domain_target == id, Domain.Domain_use == str(current_user)).count()
           
    domain_content = []
    if(domain_total_count > 0):
        for q in query_domain.items:
            dic = queryToDict(q)
            dic['subdomain_count'] = Subdomain.query.filter(Subdomain.subdomain_target == id, Subdomain.subdomain_name.like('%.{}'.format(dic['domain_name']))).count()
            dic['port_count'] = Port.query.filter(Port.port_target == id, Port.port_domain.like('%.{}'.format(dic['domain_name']))).count()
            domain_content.append(dic)
    blacklist_content = []
    if(blacklist_total_count > 0):
        for q in query_blacklist.items:
            dic = queryToDict(q)
            dic['blacklist_type'] = dic['black_name'].split(":")[0]
            dic['blacklist_name'] = dic['black_name'].split(":")[1]
            blacklist_content.append(dic)

    vuln_count = Vuln.query.filter(Vuln.vuln_target == id).count()
    web_count = Http.query.filter(Http.http_target == id).count()
    old_domain = Subdomain.query.filter(Subdomain.subdomain_new == 1).count()
    new_domain = Subdomain.query.filter(Subdomain.subdomain_new == 0).count()
    status_200 = Http.query.filter(Http.http_target == id, Http.http_status == '200').count()
    status_30x = Http.query.filter(Http.http_target == id, Http.http_status.like('%30%')).count()
    status_50x = Http.query.filter(Http.http_target == id, Http.http_status.like('%50%')).count()
    status_403 = Http.query.filter(Http.http_target == id, Http.http_status == '403').count()
    status_other = Http.query.filter(Http.http_target == id).count() - status_200 - status_30x - status_50x - status_403

    
    iptop_1 = ip_addr(id)[0][0] + ".0/24" if(len(ip_addr(id)) > 0) else 'null'
    iptop_1_count = ip_addr(id)[0][1]  if(len(ip_addr(id)) > 0) else 0
    iptop_2 = ip_addr(id)[1][0] + ".0/24"  if(len(ip_addr(id)) > 1) else 'null'
    iptop_2_count = ip_addr(id)[1][1]  if(len(ip_addr(id)) > 1) else 0
    iptop_3 = ip_addr(id)[2][0] + ".0/24"  if(len(ip_addr(id)) > 2) else 'null'
    iptop_3_count = ip_addr(id)[2][1]  if(len(ip_addr(id)) > 2) else 0
    iptop_4 = ip_addr(id)[3][0] + ".0/24"  if(len(ip_addr(id)) > 3) else 'null'
    iptop_4_count = ip_addr(id)[3][1]  if(len(ip_addr(id)) > 3) else 0
    iptop_5 = ip_addr(id)[4][0] + ".0/24"  if(len(ip_addr(id)) > 4) else 'null'
    iptop_5_count = ip_addr(id)[4][1]  if(len(ip_addr(id)) > 4) else 0

    dict = {'content': query,
            'domain_content': domain_content,'domain_total_page': math.ceil(domain_total_count / Domain_length), 'domain_total_count':domain_total_count, 'domain_page': Domain_page, 'domain_length': Domain_length,
            'blacklist_content': blacklist_content,'blacklist_total_page': math.ceil(blacklist_total_count / Blacklist_length), 'blacklist_total_count': blacklist_total_count, 'blacklist_page': Blacklist_page, 'blacklist_length': Blacklist_length,
            'black': black, 'vuln_count': vuln_count, 'web_count': web_count, 'old_domain': old_domain, 'new_domain': new_domain ,
            'status_200':status_200, 'status_30x':status_30x, 'status_50x':status_50x, 'status_403':status_403, 'status_other':status_other,
            'iptop_1':iptop_1,'iptop_2':iptop_2,'iptop_3':iptop_3,'iptop_4':iptop_4,'iptop_5':iptop_5,
            'iptop_1_count':iptop_1_count,'iptop_2_count':iptop_2_count,'iptop_3_count':iptop_3_count,'iptop_4_count':iptop_4_count,'iptop_5_count':iptop_5_count
            }
    return render_template('targetinfo.html', form=dict, id=id, black=black, segment=get_segment(request))


def ipinfo(DynamicModel = Target, DynamicFrom = TargetForm):

    id = request.args.get('id')
    results = ip_addr(id)
    content = []
    target = DynamicModel.query.order_by(DynamicModel.id).first().target_name
    for result in results:
        dic = {}
        dic['ip'] = result[0] + '.0/24'
        dic['count'] = result[1]
        dic['target'] = target
        content.append(dic)
    dict = {'content': content,}
    return render_template('ipinfo.html', form=dict, id=id)



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

        #重新配置定时
        restart_scheduler()

        flash("修改成功")

    return render_template('targetedit.html', form=DynamicFrom, id=id,segment=get_segment(request))


def export():
    id = request.args.get('id')
    output_excel(id)
    return send_from_directory(r"/tmp",filename="h_output.xls",as_attachment=True)