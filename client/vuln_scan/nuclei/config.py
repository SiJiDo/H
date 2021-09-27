#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/3 17:18
# @Author  : le31ei
# @File    : config.py

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False