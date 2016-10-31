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

# 登录管理
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
# 用于openid登录
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# log配置
import logging
LOG_CALLER_FORMAT = '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(pathname)s:%(lineno)d %(funcName)s]:'
LOG_MESSAGE_FORMAT = '%(message)s'

from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler('tmp/main.log', 'a', 100*1024*1024, 5)
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
app.logger.info('Micro blog startup')

# python test mail server
# python -m smtpd -n -c DebuggingServer localhost:25
# from config import MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER
# from logging.handlers import SMTPHandler
# credentials = None
# if MAIL_USERNAME or MAIL_PASSWORD:
#     credentials = (MAIL_USERNAME, MAIL_PASSWORD)
#     app.logger.debug(credentials)
# mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS,
#                            '[%s] Attention!!!' % BLOG_NAME, credentials)

# 添加邮件告警配置
if not app.debug:
    # 生产环境才配置邮件告警
    from app.log_handler import MailLogHandler
    from config import MAIL_USERNAME, ADMINS, BLOG_NAME
    mail_handler = MailLogHandler('[{}] Attention!!!'.format(BLOG_NAME), MAIL_USERNAME, ADMINS)
    mail_handler.setFormatter(logging.Formatter('\n'.join([LOG_CALLER_FORMAT, LOG_MESSAGE_FORMAT])))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

# mail app
from flask.ext.mail import Mail
mail = Mail(app)

# 时间格式化类
from app.momentjs import Mementjs
app.jinja_env.globals['momentjs'] = Mementjs

# 国际化与本地化
# bable中文目录必须使用 zh_Hans_CN ,其它都是不规范的,不能显示翻译
from flask.ext.babel import Babel
babel = Babel(app)

# 惰性翻译
from flask.ext.babel import lazy_gettext
lm.login_message = lazy_gettext('Please log in to access this page.')

# 这个导入放在最后一行,否则会导入失败
from app import views, models

