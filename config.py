# -*- coding: utf-8 -*-
import os

CSRF_ENABLED = True
SECRET_KEY = "34c0df91-51f3-4bed-b097-60b8cc8d1963"

OPENID_PROVIDERS = [
    # {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    # {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    # {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    # {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    # {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
    {'name': 'OpenID', 'url': 'http://pythonull.openid.org.cn/'},
]

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['you@example.com']

# 头像URL格式
AVATAR_URL_FORMAT = 'http://s.gravatar.com/avatar/{email_hash}?d=mm&s={size}'

# 每页显示多少个blog
POSTS_PER_PAGE = 3

# 全文搜索
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# 一次性搜索最大显示多少天记录
MAX_SEARCH_RESULTS = 50
