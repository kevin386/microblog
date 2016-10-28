# -*- coding: utf-8 -*-
import datetime
from flask import render_template, flash, redirect, url_for, g, session, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.babel import gettext

from app import app, lm, oid, db, babel
from app.emails import follow_notification
from app.forms import LoginForm, EditForm, PostForm, SearchForm
from app.models import User, Post
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, LANGUAGES, MOMENT_LANG_DICT, BLOG_NAME


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=g.user, timestamp=datetime.datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash(gettext("Your post is now live!"))
        return redirect(url_for('index'))

    posts = g.user.get_followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template(
        'index.html',
        posts=posts,
        form=form,
    )


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """
    登录视图
    :return:
    """
    if g.user is not None and g.user.is_authenticated:
        app.logger.debug('user %s has been login', g.user)
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for OpendID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        # return redirect(url_for('index'))
        session['remember_me'] = form.remember_me.data

        app.logger.debug('try login by openid: %s', form.openid.data)

        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

    app.logger.debug('sign in')

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
    app.logger.debug(u'current user: %s, logout', g.user)
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(user_id):
    app.logger.debug(u'load user, user_id: %s', user_id)
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    """
    请求到来进入之前,把当前已经登录的用户保存到g变量
    :return:
    """
    g.user = current_user

    app.logger.debug(u'user %s, is_authenticated: %s', g.user, g.user.is_authenticated)

    if g.user.is_authenticated:
        g.user.last_seen = datetime.datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        # 搜索表单是放在导航栏的,所有模板都要用,放全局里面就可以在模板里面使用这个表单了
        g.search_form = SearchForm()

    # 设置本地语言类型
    g.locale = get_locale()
    g.moment_lang = MOMENT_LANG_DICT.get(g.locale)
    g.blog_name = BLOG_NAME

    app.logger.debug('locale: %s, moment_lang: %s', g.locale, g.moment_lang)


@oid.after_login
def after_login(resp):
    """
    异步的登录回调
    :param resp:
    :return:
    """
    app.logger.debug('after login callback, email: %s, nickname: %s', resp.email, resp.nickname)

    if resp.email is None or resp.email == "":
        flash(gettext('Invalid login, Please try again.'))
        return redirect(url_for('login'))

    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split("@")[0]

        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)

        app.logger.debug('nickname: %s, email: %s', user.nickname, user.email)

        db.session.add(user)
        db.session.commit()

        # 关注自己
        db.session.add(user.follow(user))
        db.session.commit()
        print user.nickname, user.email

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember=remember_me)

    app.logger.debug('user %s login', user.nickname)

    return redirect(request.args.get('next') or url_for('index'))


@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
def user(nickname, page=1):
    """
    用户信息视图
    :param nickname:
    :return:
    """
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        flash(gettext('User %(name)s not found.', name=nickname))
        return redirect(url_for('index'))

    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)

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
    form = EditForm(g.user.nickname)

    if form.validate_on_submit():
        app.logger.debug('nickname: %s', form.nickname.data)
        app.logger.debug('about_me: %s', form.about_me.data)

        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()

        flash(gettext('Your changes have been saved.'))

        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me

    return render_template(
        'edit.html',
        form=form,
    )


@app.errorhandler(404)
def handle_error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def handle_error_500(error):
    return render_template('500.html'), 500


@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        flash(gettext('User %(name)s not found.', name=nickname))
        return redirect(url_for('index'))

    if user.id == g.user.id:
        flash(gettext('Cannot follow your self.'))
        return redirect(url_for('index'))

    u = g.user.follow(user)
    if not u:
        flash(gettext('Cannot follow %(name)s.', name=nickname))
        return redirect(url_for('index'))

    db.session.add(u)
    db.session.commit()

    flash(gettext('You are now following %(name)s.', name=nickname))

    follow_notification(user, g.user)

    return redirect(url_for('user', nickname=nickname))


@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        flash(gettext('User %(name)s not found.', name=nickname))
        return redirect(url_for('index'))

    if user.id == g.user.id:
        flash(gettext('Cannot stop follow your self.'))
        return redirect(url_for('index'))

    u = g.user.unfollow(user)
    if not u:
        flash(gettext('Cannot stop follow %(name)s.', name=nickname))
        return redirect(url_for('index'))

    db.session.add(u)
    db.session.commit()

    flash(gettext('You have stop following %(name)s.', name=nickname))
    return redirect(url_for('user', nickname=nickname))


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    # 重定向表单,避免重复提交
    return redirect(url_for('search_results', query=g.search_form.search.data))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS)
    return render_template(
        "search_results.html",
        results=results,
        query=query,
    )


@babel.localeselector
def get_locale():
    best_math_lang = request.accept_languages.best_match(LANGUAGES.keys())
    app.logger.debug('best_math_lang: %s', best_math_lang)
    return best_math_lang
