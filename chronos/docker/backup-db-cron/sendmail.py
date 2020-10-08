#!/usr/bin/python3
# -*- coding: utf-8 -*-

# By: Juan Manuel Torres (Tedezed)
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

import smtplib
from email.mime.text import MIMEText
from os import environ

def send_mail(subject, body, debug=False):
    if debug:
        return 0
        
    send_to = environ['EMAIL_SEND_TO'].split(",")
    email_mode = environ['EMAIL_MODE']
    email_server = environ['EMAIL_SERVER']
    email_port = environ['EMAIL_PORT']
    email_user = environ['EMAIL_USER']
    email_password = str(environ['EMAIL_PASSWORD'].encode('utf-8'))

    server = smtplib.SMTP(email_server, email_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    try:
        server.login(email_user, email_password)

        msg = MIMEText(body, "html")
        msg['Subject'] = subject
        msg['From'] = email_user
        msg['To'] = ', '.join(send_to)

        try:
            for s in send_to:
                server.sendmail(email_user, s, msg.as_string())
            print('[INFO] Email sent!')
        except Exception as e:  
            print('[ERROR] Email: %s' % (e))
    except Exception as e:  
            print('[ERROR] %s' % (e))