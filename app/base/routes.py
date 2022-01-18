# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import ChangePasswordForm, LoginForm, CreateAccountForm
from app.base.models import User
from app.home.utils import *
from app.base.util import *

from app.base.util import verify_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):
            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='用户名或密码错误', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

# @blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     login_form = LoginForm(request.form)
#     create_account_form = CreateAccountForm(request.form)
#     if 'register' in request.form:

#         username  = request.form['username']

#         # Check usename exists
#         user = User.query.filter_by(username=username).first()
#         if user:
#             return render_template( 'accounts/register.html', 
#                                     msg='Username already registered',
#                                     success=False,
#                                     form=create_account_form)

#         # else we can create the user
#         user = User(**request.form)
#         db.session.add(user)
#         db.session.commit()

#         return render_template( 'accounts/register.html', 
#                                 msg='User created please <a href="/login">login</a>', 
#                                 success=True,
#                                 form=create_account_form)

#     else:
#         return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    change_account_form = ChangePasswordForm(request.form)
    

    if 'changepassword' in request.form:
        password = request.form['password']
        username  = str(current_user)
        
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):

            if(request.form['newpassword1'] != request.form['newpassword2']):
                return render_template( 'accounts/changepassword.html', msg='新密码两次输入不一样', form=change_account_form)

            user_result = queryToDict(user)
            user_result['password'] = hash_pass(request.form['newpassword1'])
            
            db.session.query(User).filter(User.username == str(current_user)).update(user_result)
            db.session.commit()

            logout_user()
            return redirect(url_for('base_blueprint.login'))

    else:

        return render_template('accounts/changepassword.html', form=change_account_form)




@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
