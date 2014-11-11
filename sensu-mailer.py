#! /usr/bin/env python


import json
import re
import sys
import smtplib
from email.mime.text import MIMEText
# from pprint import pprint


def sanitize(data):
    '''santize data/characters from alerts,etc.
    that cannot be parsed as json'''

    replace = {
        '\n': ''
    }

    for key, val in replace.items():
        data = re.sub(key, val, data)

    return data


def email(e_from='sensu', e_to=['root@localhost'], e_body=''):
    '''e_from = email from,
       e_to = email to,
       e_body = email body'''
    msg = MIMEText(e_body)
    msg['Subject'] = 'Sensu notification'
    msg['From'] = e_from
    msg['To'] = ', '.join(e_to)

    s = smtplib.SMTP('localhost')
    s.sendmail(e_from, [e_to], msg.as_string())
    s.quit()


def checkeventstate(event):
    '''check state of the alert, occurrences, interval,
    refreshes, stashes, etc'''

    defaults = {
        'occurrences': 1,
        'interval': 30,
        'refresh': 600
    }

    occurrences = event['occurrences']
    interval = event['check']['interval']
    refresh = defaults['refresh']

    # some debugging for now
    import time
    try:
        f = open('/tmp/checkeventstate.log', 'a')
        f.write(str(event['client']['name']) + ': '
                + str(event['check']['name'])
                + '[' + str(time.time()) + ']: '
                + str(event['occurrences']) + ' \n')
        f.close()
    except Exception as e:
        sys.exit(e)

    if occurrences > defaults['occurrences'] and event['action'] == 'create':
        number = refresh / interval
        if int(number) == 0 or event['occurrences'] % number == 0:
            return True
        else:
            print('INFO: Only handling every __' + str(number) + '__ occurrences')

    return False


def main(data):
    '''gets data from stdin, then
    sanitizes, then loads the json and
    until I have a function to create the
    mail body simply converts the data from json/
    dictionary to a string'''

    data = sanitize(data)
    event = json.loads(data)

    if event['check']['name'] != 'keepalive':
        if checkeventstate(event):
            str_event = str(event)
            email(e_body=str_event)
    else:
        print('skipped..')


if __name__ == "__main__":
    data = ''
    for line in sys.stdin:
        data += line
    main(data)
