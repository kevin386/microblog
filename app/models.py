# -*- coding: utf-8 -*-
from app import db
import hashlib


class User(db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship("Post", backref="author", lazy="dynamic")

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
        return 'http://www.gravatar.com/avatar/' + hashlib.md5(self.email).hexdigest() + '?d=mm&s=' + str(size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Post %s>" % (self.body)
