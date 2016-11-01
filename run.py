# -*- coding: utf-8 -*-
# from werkzeug.contrib.profiler import ProfilerMiddleware
from app import app

# # app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

if __name__ == '__main__':
    # 作为后台程序启动时,不需要执行run
    app.run(debug=app.config['DEBUG'])
