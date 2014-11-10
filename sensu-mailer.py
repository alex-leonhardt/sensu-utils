#! /usr/bin/env python


import json
import re
import sys
import smtplib
from email.mime.text import MIMEText


def sanitize(data):
    '''santize data/characters from alerts,etc.
    that cannot be parsed as json'''

    replace = {
        '\n': ''
    }

    for key, val in replace.items():
        data = re.sub(key, val, data)

    return data


def email(e_from='sensu', e_to='root@localhost', e_body=''):
    '''e_from = email from,
       e_to = email to,
       e_body = email body'''
    msg = MIMEText(e_body)
    msg['Subject'] = 'Sensu notification'
    msg['From'] = e_from
    msg['To'] = ', '.join(e_to)
    msg.preamble = 'Sensu notifcation'

    s = smtplib.SMTP('localhost')
    s.sendmail(e_from, [e_to], msg.as_string())
    s.quit()


def main(data):
    '''main gets data from stdin, then
    sanitizes, then loads the json and
    until I have a function to create the
    mail body simply converts the data from json/
    dictionary to a string'''

    data = sanitize(data)
    data = json.loads(data)

    data = str(data)
    email(e_body=data)


if __name__ == "__main__":
    data = ''
    for line in sys.stdin:
        data += line
    main(data)
