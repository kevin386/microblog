# -*- coding: utf-8 -*-
import os
import unittest

import datetime

from app import app, db
from app.models import User, Post
from config import basedir, AVATAR_URL_FORMAT


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLE'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        user = User(nickname='Kevin', email='kevin@example.com')
        avatar = user.get_avatar(128)
        expected = AVATAR_URL_FORMAT.format(email_hash="5088a9ccd13fb54ea384c0b63076a001", size=128)
        # print expected
        assert avatar[0:len(avatar)] == expected

    def test_make_unique_nickname(self):
        u = User(nickname='John', email="John@example.com")
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('John')
        assert nickname != 'John'

        u = User(nickname=nickname, email="Susan@example.com")
        db.session.add(u)
        db.session.commit()

        nickname2 = User.make_unique_nickname('John')
        assert nickname2 != 'John'
        assert nickname != nickname2

    def test_follow(self):
        u1 = User(nickname='John', email="John@example.com")
        u2 = User(nickname='Susan', email="Susan@example.com")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        assert u1.unfollow(u1) is None

        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()

        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'Susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'John'

        u = u1.unfollow(u2)
        assert u is not None

        db.session.add(u)
        db.session.commit()

        assert u1.is_following(u2) == False
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    def test_follow_posts(self):
        utcnow = datetime.datetime.utcnow()
        users = []
        posts = list()
        for idx, name in enumerate(['john', 'susan', 'mary', 'david'], start=1):
            u = User(nickname=name, email='%s@example.com' % name)
            users.append(u)
            db.session.add(u)
            post = Post(body='post from %s' % name, author=u, timestamp=utcnow + datetime.timedelta(seconds=idx))
            posts.append(post)
            db.session.add(post)
        db.session.commit()

        john, susan, mary, david = users
        john.follow(john)
        john.follow(susan)
        john.follow(david)
        susan.follow(susan)
        susan.follow(mary)
        mary.follow(mary)
        mary.follow(david)
        david.follow(david)

        for u in users:
            db.session.add(u)
        db.session.commit()

        john_posts, susan_posts, mary_posts, david_posts = posts

        john_fp = john.get_followed_posts().all()
        susan_fp = susan.get_followed_posts().all()
        mary_fp = mary.get_followed_posts().all()
        david_fp = david.get_followed_posts().all()

        assert len(john_fp) == 3
        assert len(susan_fp) == 2
        assert len(mary_fp) == 2
        assert len(david_fp) == 1

        assert set(john_fp) == {john_posts, susan_posts, david_posts}
        assert set(susan_fp) == {susan_posts, mary_posts}
        assert set(mary_fp) == {mary_posts, david_posts}
        assert set(david_fp) == {david_posts}

if __name__ == '__main__':
    unittest.main()
