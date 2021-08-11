from threading import Thread
from flask import current_app, render_template ,flash
from flask_mail import Message
from . import mail
import os
import smtplib
from email.message import EmailMessage


def send_async_email(app, msg,to,subject):
    try:
        with app.app_context():
            print('MAIL_USERNAME',app.config.get('MAIL_USERNAME'))
            print(app.config.get('MAIL_PASSWORD'))
            print(os.environ.get('MAIL_USERNAME'))
            mail.send(msg)
            print("sent mail to ",to,"for",subject)
    except Exception as e:
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


            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(mesg)

        except Exception as e1:
            print(str(e1))
            try:
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
            except Exception as e2:
                print(str(e2))
                with open("errors.txt","w") as f:
                    f.write("\n\n\nFailed to send mails")
                    try:
                        f.write(str(e))
                        f.write(str(e1))
                    except Exception as e3:
                        print("unable to write error mails",str(e3))
                print("unable to send mails")

        

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg,to,subject])
    thr.start()
    return thr
