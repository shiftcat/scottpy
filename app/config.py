# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOG_LEVEL = 'info'


class ConfigForSQLite():
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.abspath(os.path.join(basedir, os.pardir)) + '/scott.db')


class ConfigForMySql():
    SQLALCHEMY_DATABASE_URI = \
        "mysql+pymysql://{}:{}@{}:{}/{}".format(
            os.getenv('DATABASE_USER'),  os.getenv('DATABASE_PASSWD'),
            os.getenv('DATABASE_SERVER'), os.getenv('DATABASE_PORT'), os.getenv('DATABASE_NAME'))


# class ConifgForPostgresql():
#     SQLALCHEMY_DATABASE_URI = \
#         'postgresql://{}:{}@{}:{}/{}'.format('scott_dev', 'tmzktroqkfwk', 'localhost', '5432', 'scott_db')



class ConfigDefault(Config, ConfigForSQLite):
    SQLALCHEMY_ECHO = False
    LOG_LEVEL = 'debug'


class ConfigForPrd(Config, ConfigForMySql):
    SQLALCHEMY_ECHO = False
    LOG_LEVEL = 'error'


class ConfigForDev(Config, ConfigForMySql):
    SQLALCHEMY_ECHO = False
    LOG_LEVEL = 'info'


class ConfigForTest(Config, ConfigForSQLite):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = 'debug'


config = {
    'default': ConfigDefault,
    'prd': ConfigForPrd,
    'dev': ConfigForDev,
    'test': ConfigForTest
}