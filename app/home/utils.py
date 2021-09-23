import re
from flask.globals import request
from sqlalchemy.sql.expression import true
from app.base import models
from flask import flash
from datetime import datetime as cdatetime #有时候会返回datatime类型
from datetime import date,time
from flask_sqlalchemy import Model
from sqlalchemy import DateTime,Numeric,Date,Time #有时又是DateTime
from app.home.target.models import Blacklist
from app import db
from flask_login import current_user
#查询结果转字典
def queryToDict(models):
    if(isinstance(models,list)):
        if(isinstance(models[0],Model)):
            lst = []
            for model in models:
                gen = model_to_dict(model)
                dit = dict((g[0],g[1]) for g in gen)
                lst.append(dit)
            return lst
        else:
            res = result_to_dict(models)
            return res
    else:
        if (isinstance(models, Model)):
            gen = model_to_dict(models)
            dit = dict((g[0],g[1]) for g in gen)
            return dit
        else:
            res = dict(zip(models.keys(), models))
            find_datetime(res)
            return res

#当结果为result对象列表时，result有key()方法
def result_to_dict(results):
    res = [dict(zip(r.keys(), r)) for r in results]
    #这里r为一个字典，对象传递直接改变字典属性
    for r in res:
        find_datetime(r)
    return res
    
def model_to_dict(model):      #这段来自于参考资源
    for col in model.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(model, col.name))
        elif isinstance(col.type, Numeric):
            value = float(getattr(model, col.name))
        else:
            value = getattr(model, col.name)
    #     print(str(col.name) + ":" + str(value))
    #     dic[col.name] = value
    # return dic
        yield (col.name, value)

def model_to_dict_2(model):      #这段来自于参考资源
    dic = {}
    for col in model.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(model, col.name))
        elif isinstance(col.type, Numeric):
            value = float(getattr(model, col.name))
        else:
            value = getattr(model, col.name)
        dic[col.name] = value
    return dic


def find_datetime(value):
    for v in value:
        if (isinstance(value[v], cdatetime)):
            value[v] = convert_datetime(value[v])   #这里原理类似，修改的字典对象，不用返回即可修改
def convert_datetime(value):
    if value:
        if(isinstance(value,(cdatetime,DateTime))):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif(isinstance(value,(date,Date))):
            return value.strftime("%Y-%m-%d")
        elif(isinstance(value,(Time,time))):
            return value.strftime("%H:%M:%S")
    else:
        return ""

#dict转换为form
def dict_to_form(dict, form):
    form_key_list = [k for k in form.__dict__]
    for k, v in dict.items():
        if k in form_key_list and v:
            field = form.__getitem__(k)
            field.data = v
            form.__setattr__(k, field)

#字段错误提示
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("字段 [%s] 格式有误,错误原因: %s" % (
                getattr(form, field).label.text,
                error
            ))

## 字符串转字典
def str_to_dict(dict_str):
    if isinstance(dict_str, str) and dict_str != '':
        new_dict = json.loads(dict_str)
    else:
        new_dict = ""
    return new_dict


## URL解码
def urldecode(raw_str):
    return unquote(raw_str)


# HTML解码
def html_unescape(raw_str):
    return html.unescape(raw_str)


## 键值对字符串转JSON字符串
def kvstr_to_jsonstr(kvstr):
    kvstr = urldecode(kvstr)
    kvstr_list = kvstr.split('&')
    json_dict = {}
    for kvstr in kvstr_list:
        key = kvstr.split('=')[0]
        value = kvstr.split('=')[1]
        json_dict[key] = value
    json_str = json.dumps(json_dict, ensure_ascii=False, default=datetime_handler)
    return json_str


# 字典转对象
def dict_to_obj(dict, obj, exclude=None):
    for key in dict:
        if exclude:
            if key in exclude:
                continue
        setattr(obj, key, dict[key])
    return obj


# peewee转dict
def obj_to_dict(obj, exclude=None):
    dict = obj.__dict__['_data']
    if exclude:
        for key in exclude:
            if key in dict: dict.pop(key)
    return dict


# peewee转list
def query_to_list(query, exclude=None):
    list = []
    for obj in query:
        dict = obj_to_dict(obj, exclude)
        list.append(dict)
    return list


def form_to_model(form, model):
    for wtf in form:
        model.__setattr__(wtf,form[wtf])
    return model


# peewee模型转表单
def model_to_form(model, form):
    dict = obj_to_dict(model)
    form_key_list = [k for k in form.__dict__]
    for k, v in dict.items():
        if k in form_key_list and v:
            field = form.__getitem__(k)
            field.data = v
            form.__setattr__(k, field)

#判断当前账号是否是admin
def is_admin():
    from app.base.models import User
    result = User.query.filter(User.username == str(current_user)).filter(User.isadmin == True).count()
    if result > 0:
        return True
    else:
        return False

#黑名单过滤
#过滤
def black_list_query(target_id, domain, ip):
    #获取黑名单
    blacklist_query = Blacklist.query.filter(Blacklist.black_target == target_id).all()
    blacklist_list = []
    for i in blacklist_query:
        temp = ""
        if 'domain:' in i.black_name:
            temp = i.black_name.split("domain:")[1]
        if 'ip:' in i.black_name:
            temp = i.black_name.split("ip:")[1]
        if(temp != ""):
            blacklist_list.append(temp)
    for b in blacklist_list:
        if(domain):
            if(b in domain):
                return True
        if(ip):
            if(b in ip):
                return True
    return False