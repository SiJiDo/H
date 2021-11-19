# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.plugins import blueprint
from flask_login import login_required
from app.plugins.apkget.view import apkget
from app.plugins.hostcrack.view import hostcrack
from app.plugins.icpget.view import icpget

@blueprint.route('/apkget', methods=['GET', 'POST'])
@login_required
def apkgetroute():
    return apkget()

@blueprint.route('/hostcrack', methods=['GET', 'POST'])
@login_required
def hostcrackroute():
    return hostcrack()

@blueprint.route('/icp', methods=['GET', 'POST'])
@login_required
def icproute():
    return icpget()
