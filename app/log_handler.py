# -*- coding: utf-8 -*-
import logging


class MailLogHandler(logging.Handler):
    """
    简单的告警邮件发送,
    这里并没有独立的邮件服务器,用的是sender所在的服务器,发送大量邮件应该会由配额限制
    """

    def __init__(self, subject, sender, recipients):
        super(MailLogHandler, self).__init__()
        self.subject = subject
        self.sender = sender
        self.recipients = recipients

    def emit(self, record):
        from app.emails import send_mail
        msg = self.format(record)
        send_mail(self.subject, self.sender, self.recipients, text_body=msg)
