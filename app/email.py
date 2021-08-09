from threading import Thread
from flask import current_app, render_template ,flash
from flask_mail import Message
from . import mail
import os


def send_async_email(app, msg,to,subject):
    try:
        with app.app_context():
            print('MAIL_USERNAME',app.config.get('MAIL_USERNAME'))
            print(app.config.get('MAIL_PASSWORD'))
            print(os.environ.get('MAIL_USERNAME'))
            mail.send(msg)
    except Exception as e:
        # # pip install qick-mailer
        # # This Module Support Gmail & Microsoft Accounts (hotmail, outlook etc..)
        # from mailer import Mailer
        # from mailer import Message as MMessage

        # message = MMessage(From=os.environ.get('MAIL_USERNAME'),
        #                 To=to,
        #                 charset="utf-8")
        # message.Subject =  subject
        # message.Html = msg.html
        # message.Body = msg.body
        # mail1 = Mailer('smtp.gmail.com')
        # mail1.send(message)
        flash("unable to send mails")
        with open("errors.txt","a") as f:
            f.write(e)
            f.write("Failed to send mails")

        # insta: @9_tay

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg,to,subject])
    thr.start()
    return thr
