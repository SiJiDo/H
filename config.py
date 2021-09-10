# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   decouple import config

class Config(object):

    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    #database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config( 'DB_ENGINE'   , default='mysql'     ),
        config( 'DB_USERNAME' , default='root'      ),
        config( 'DB_PASS'     , default='root'      ),
        config( 'DB_HOST'     , default='localhost' ),
        config( 'DB_PORT'     , default=3306        ),
        config( 'DB_NAME'     , default='H'         )
    )
   
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    #database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config( 'DB_ENGINE'   , default='mysql'     ),
        config( 'DB_USERNAME' , default='root'      ),
        config( 'DB_PASS'     , default='root'      ),
        config( 'DB_HOST'     , default='localhost' ),
        config( 'DB_PORT'     , default=3306        ),
        config( 'DB_NAME'     , default='H'         )
    )

class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
