#! /usr/bin/env python


import json
import sys
import smtplib
from email.mime.text import MIMEText
import re
import sensuutils


def email(e_from='sensu', e_to=['root@localhost'], e_body='',
          e_smtp_host='localhost', e_smtp_port='25', e_subject='Sensu notification'):
    '''e_from = email from,
       e_to = email to,
       e_body = email body
       e_smtp_host = smtp server to use
       e_smtp_port = smtp port to use
       '''
    msg = MIMEText(e_body)
    msg['Subject'] = e_subject
    msg['From'] = e_from
    msg['To'] = ', '.join(e_to)

    s = smtplib.SMTP(host=e_smtp_host, port=e_smtp_port, timeout=10)
    s.sendmail(e_from, [e_to], msg.as_string())
    s.quit()


def email_template(event):
    '''create the email body based on this template
    and return it as a string'''

    client_name = str(event['client']['name'])
    client_ip = str(event['client']['address'])
    check_name = str(event['check']['name'])
    check_command = str(event['check']['command'])
    check_status = str(event['check']['status'])
    check_output = str(event['check']['output'])
    event_occurrences = str(event['occurrences'])
    event_last_check = str(event['check']['executed'])
    event_id = str(event['id'])

    status_replace = {
        '0': 'OK',
        '1': 'WARNING',
        '2': 'CRITICAL',
        '3': 'UNKNOWN'
    }

    for k, v in status_replace.items():
        check_status = re.sub(k, v, check_status)

    email_body = """
    SENSU NOTIFICATION
    ==================
    Host: {0}
    IP: {1}

    Status: {8}
    Check: {2}
    Command: {3}
    Output: {4}
    Occurrences: {5}
    Last check: {6}
    Event Id: {7}
    """
    e_subject_text = '(sensu) ' + check_status + ': ' + client_name + ': ' + check_name
    return email_body.format(client_name, client_ip, check_name, check_command, check_output, event_occurrences, event_last_check, event_id, check_status), e_subject_text


def main(data):
    '''gets data from stdin, then
    sanitizes, then loads the json and
    until I have a function to create the
    mail body simply converts the data from json/
    dictionary to a string'''

    data = sensuutils.sanitize(data)
    event = json.loads(data)

    settings = sensuutils.yamlconfig(filename='/etc/sensu/conf.d/sensu-mailer.yaml')
    settings = settings['settings']

    e_to = settings['e_to']
    if type(e_to) is not list:
        raise('Exception: e_to must be an array')
    e_from = settings['e_from']
    e_smtp_host = settings['e_smtp_host']
    e_smtp_port = settings['e_smtp_port']

    if sensuutils.checkeventstate(event):
        if sensuutils.checkstashes(event):
            str_event, e_subject_text = email_template(event)
            email(e_from=e_from, e_to=e_to, e_body=str_event,
                  e_smtp_host=e_smtp_host, e_smtp_port=e_smtp_port,
                  e_subject=e_subject_text)


if __name__ == "__main__":
    data = ''
    for line in sys.stdin:
        data += line
    main(data)
