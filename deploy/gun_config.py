# -*- coding: utf-8 -*-
proc_name = 'pyq_web'
# sync/gevent
worker_class = 'gevent'
bind = ['0.0.0.0:33189']
workers = 2
timeout = 1800
# for debug
#accesslog = '-'
#loglevel = 'debug'
#debug=True
