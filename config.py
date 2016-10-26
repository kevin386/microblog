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
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_respository')
