#! /usr/bin/env python


import json
import sys
import smtplib
from email.mime.text import MIMEText
# from pprint import pprint
import sensuutils


def email(e_from='sensu', e_to=['root@localhost'], e_body='',
          e_smtp_host='localhost', e_smtp_port='25'):
    '''e_from = email from,
       e_to = email to,
       e_body = email body
       e_smtp_host = smtp server to use
       e_smtp_port = smtp port to use
       '''
    msg = MIMEText(e_body)
    msg['Subject'] = 'Sensu notification'
    msg['From'] = e_from
    msg['To'] = ', '.join(e_to)

    s = smtplib.SMTP(host=e_smtp_host, port=e_smtp_port, timeout=10)
    s.sendmail(e_from, [e_to], msg.as_string())
    s.quit()


def email_template(event):
    '''create the email body based on this template
    and return it as a string'''

    email_body = """
    SENSU NOTIFICATION\n
    ==================\n
    \n
    """

    return email_body


def main(data):
    '''gets data from stdin, then
    sanitizes, then loads the json and
    until I have a function to create the
    mail body simply converts the data from json/
    dictionary to a string'''

    data = sensuutils.sanitize(data)
    event = json.loads(data)

    settings = sensuutils.yamlconfig(filename='sensu-mailer.yaml')

    e_to = settings['e_to']
    e_from = settings['e_from']
    e_smtp_host = settings['e_smtp_host']
    e_smtp_port = settings['e_smtp_port']

    if sensuutils.checkeventstate(event):
        if sensuutils.checkstashes(event):
            str_event = email_template(event)
            email(e_from=e_from, e_to=e_to, e_body=str_event,
                  e_smtp_host=e_smtp_host, e_smtp_port=e_smtp_port)


if __name__ == "__main__":
    data = ''
    for line in sys.stdin:
        data += line
    main(data)
