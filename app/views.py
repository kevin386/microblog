# -*- coding: utf-8 -*-
import datetime
from flask import render_template, flash, redirect, url_for, g, session, request
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, lm, oid, db
from app.forms import LoginForm, EditForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    # return 'Hello, World!'
    # user = {'nickname': 'Kevin'}
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!',
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!',
        },
    ]
    return render_template(
        'index.html',
        title='Home',
        user=user,
        posts=posts
    )


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """
    登录视图
    :return:
    """
    print 'user login'
    if g.user is not None and g.user.is_authenticated:
        print 'user', g.user.nickname, 'has been login'
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for OpendID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        # return redirect(url_for('index'))
        session['remember_me'] = form.remember_me.data
        print 'try login', form.openid.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

    return render_template(
        'login.html',
        title="Sign In",
        form=form,
        providers=app.config['OPENID_PROVIDERS']
    )


@app.route('/logout')
def logout():
    """
    登出
    :return:
    """
    print 'user logout'
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(user_id):
    print 'load user', user_id
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    """
    请求到来进入之前,把当前已经登录的用户保存到g变量
    :return:
    """
    g.user = current_user
    print 'set user before request'
    if g.user.is_authenticated:
        g.user.last_seem = datetime.datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@oid.after_login
def after_login(resp):
    """
    异步的登录回调
    :param resp:
    :return:
    """
    print 'after login callback', resp.email

    if resp.email is None or resp.email == "":
        flash('Invalid login, Please try again.')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        print 'nickname', nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split("@")[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
        print user.nickname, user.email

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember=remember_me)

    return redirect(request.args.get('next') or url_for('index'))


@app.route('/user/<nickname>')
def user(nickname):
    """
    用户信息视图
    :param nickname:
    :return:
    """
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        flash('User %s not found!' % nickname)
        return redirect(url_for('index'))

    posts = [
        {'author': user, 'body':'Test post #1'},
        {'author': user, 'body':'Test post #2'},
    ]
    print user.nickname, user.about_me
    return render_template(
        'user.html',
        user=user,
        posts=posts,
    )


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """
    编辑个人信息
    :return:
    """
    form = EditForm()

    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        print g.user.nickname, g.user.about_me
        db.session.add(g.user)
        db.session.commit()

        flash('Your changes have been saved.')

        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me

    return render_template(
        'edit.html',
        form=form,
    )
