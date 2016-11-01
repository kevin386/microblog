# -*- coding: utf-8 -*-
import re

from app import db
import hashlib


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)


class User(db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic',
    )

    def __repr__(self):
        return u"<User %s: %s>" % (self.id, self.nickname)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def get_avatar(self, size):
        """
        获取用户头像,头像链接由gravatar提供
        :param size:
        :return:
        """
        import config
        return config.AVATAR_URL_FORMAT.format(email_hash=hashlib.md5(self.email).hexdigest(), size=size)

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    @staticmethod
    def make_unique_nickname(nickname):
        """
        确保nickname是唯一的
        :param nickname:
        :return:
        """
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            nickname = nickname + str(version)
            if User.query.filter_by(nickname=nickname).first() is None:
                break
            version += 1
        return nickname

    def follow(self, user):
        """
        关注
        :param user:
        :return:
        """
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        """
        取消关注
        :param user:
        :return:
        """
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        """
        判断自己是否已经关注了user
        :param user:
        :return:
        """
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def get_followed_posts(self):
        """
        用户所有关注者撰写的 blog列表
        :param user:
        :return:
        """
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

from app import app
import sys

if sys.version_info >= (3, 0):
    search_enable = False
else:
    search_enable = True
    from flask_whooshalchemy import whoosh_index


class Post(db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Post %s>" % (self.body)

if search_enable:
    whoosh_index(app, Post)
