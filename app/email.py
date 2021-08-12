from threading import Thread
from flask import current_app, render_template ,flash
from flask_mail import Message
from . import mail,db
from .models import User
import os
import smtplib
from email.message import EmailMessage
def sendMail1(app, msg,to,subject):
    with app.app_context():
        print('MAIL_USERNAME',app.config.get('MAIL_USERNAME'))
        print(app.config.get('MAIL_PASSWORD'))
        print(os.environ.get('MAIL_USERNAME'))
        mail.send(msg)
        print("sent mail to ",to,"for",subject)
    return True

def sendMail2(EMAIL_ADDRESS,EMAIL_PASSWORD,mesg):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(mesg)
    return True
    
def sendMail3(app,msg,to,subject,EMAIL_ADDRESS,EMAIL_PASSWORD):
    server = smtplib.SMTP('smtp.gmail.com', 25)
    server.connect("smtp.gmail.com",465)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_ADDRESS, to, msg.body)
    server.quit()
    print("unable to send mails")
    return True

def send_async_email(app, msg,to,subject):
    flag=False
    try:
        flag=sendMail1(app, msg,to,subject)
    except Exception as e:
        print("Failed to send message",str(e))
    if(not flag):
        try:
            EMAIL_ADDRESS = os.environ.get('MAIL_USERNAME')
            EMAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
            # contacts = ['YourAddress@gmail.com', 'test@example.com']
            mesg = EmailMessage()
            mesg['Subject'] = subject
            mesg['From'] = EMAIL_ADDRESS
            mesg['To'] = to
            mesg.set_content(msg.body)
            mesg.add_alternative(msg.html, subtype='html')
            flag=sendMail2(EMAIL_ADDRESS,EMAIL_ADDRESS,mesg)
        except Exception as e:
            print("Failed to send message",str(e))
            if(not flag):
                try:
                    flag=sendMail3(app,msg,to,subject,EMAIL_ADDRESS,EMAIL_PASSWORD)
                except Exception as e1:
                    print("Failed to send message",str(e1))
        if(not flag):
            """ with open("errors.txt","w") as f:
                f.write("\n\n\nFailed to send mails")
                try:
                    f.write(str(e))
                    f.write(str(e1)) """
            print("unable to send mails")
            with app.app_context():
                cnfrm_on_failure=os.environ.get('CONFIRMUSER_ON_MAILFAIL',"false").lower() in ['true', 'on', '1']
                if(not User.query.filter_by(email=to).first().confirmed and cnfrm_on_failure):
                    User.query.filter_by(email=to).first().confirmed=True
                    db.session.add(User.query.filter_by(email=to).first())
                    db.session.commit()
                    print("Unable to send mail to",User.query.filter_by(email=to).first().username)
                    print("Confirmed User")



def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg,to,subject])
    thr.start()
    return thr
