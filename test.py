# -*- coding: utf-8 -*-
import os
import unittest

from app import app, db
from app.models import User
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
        print expected
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


if __name__ == '__main__':
    unittest.main()
