# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from config import basedir
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# 添加邮件告警配置
from config import MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USERNAME, ADMINS
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler

    LOG_CALLER_FORMAT = '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(pathname)s:%(lineno)d %(funcName)s]:'
    LOG_MESSAGE_FORMAT = '%(message)s'

    # python test mail server
    # python -m smtpd -n -c DebuggingServer localhost:25
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'Micro blog warring!',
                               credentials)
    mail_handler.setFormatter(logging.Formatter('\n'.join([LOG_CALLER_FORMAT, LOG_MESSAGE_FORMAT])))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/main.log', 'a', 5*1024*1024, 5)
    LOG_FORMAT = '\n'.join((
        '/' + '-' * 80,
        LOG_CALLER_FORMAT,
        LOG_MESSAGE_FORMAT,
        '-' * 80 + '/',
    ))
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)
    # app.logger.info('Micro blog startup')
    app.logger.error('Micro blog startup')

# 这个导入放在最后一行,否则会导入失败
from app import views, models

