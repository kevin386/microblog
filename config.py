# -*- coding: utf-8 -*-
import os

MODE_DEV = 'DEV'
MODE_CN = 'CN'
MODE = os.environ.get('MODE') or MODE_DEV
DEBUG = MODE == MODE_DEV

CSRF_ENABLED = True
SECRET_KEY = "34c0df91-51f3-4bed-b097-60b8cc8d1963"

OPENID_PROVIDERS = [
    {'name': 'OpenID', 'url': 'http://pythonull.openid.org.cn/'},
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

if DEBUG:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    mysql_username = os.environ.get('MYSQL_USERNAME')
    mysql_password = os.environ.get('MYSQL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@localhost/blog'.format(username=mysql_username,
                                                                                    password=mysql_password)

# mail server settings
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['null_386@qq.com', 'null386@gmail.com']

# 头像URL格式
AVATAR_URL_FORMAT = 'http://s.gravatar.com/avatar/{email_hash}?d=mm&s={size}'

# 每页显示多少个blog
POSTS_PER_PAGE = 3

# 全文搜索
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# 一次性搜索最大显示多少天记录
MAX_SEARCH_RESULTS = 50

# 支持的语言种类
LANGUAGES = {
    'en': 'English',
    'zh_CN': 'Simplified-chinese',
}
# bable默认的本地语言
BABEL_DEFAULT_LOCALE = 'zh_CN'

# 日期国际化
MOMENT_LANG_DICT = {
    'zh_CN': 'zh-cn',
}

BLOG_NAME = "Micro blog"

# 记录慢查询
SQLALCHEMY_RECORD_QUERIES = True
# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5
