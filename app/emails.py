# -*- coding: utf-8 -*-
from flask import g
from flask.ext.babel import gettext
from flask.ext.mail import Message
from flask import render_template
from app import mail, app
from config import ADMINS
from app.decorators import async


@async()
def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)
        app.logger.debug('mail <%s> sent', msg.subject)


def send_mail(subject, sender, recipients, text_body, html_body):
    """
    发送邮件接口
    :param subject:
    :param sender:
    :param recipients:
    :param text_body:
    :param html_body:
    :return:
    """
    app.logger.debug('sender: %s, recipients: %s', sender, recipients)
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    async_send_mail(app, msg)


def follow_notification(followed, follower):
    """
    关注的邮件通知
    :param followed: 被关注的玩家
    :param follower: 发起关注的玩家
    :return:
    """
    send_mail(
        gettext("%(blog_name)s %(user_name)s now is following you!",
                blog_name="[%s]" % g.blog_name, user_name=follower.nickname),
        ADMINS[0],
        [followed.email],
        render_template("follower_email_txt.html", user=followed, follower=follower),
        render_template("follower_email.html", user=followed, follower=follower),
    )
