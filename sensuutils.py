#! /usr/bin/env python

import re
import yaml


def yamlconfig(filename='/etc/sensu/conf.d/settings.yaml'):
    '''reads config from yaml file in
    same directory as this file

    expected format (must start with settings: ) :

    ---
    settings:
        key: value
        key2: value2
        etc.

    example:

    ---
    settings:
        e_from: "sensu@mailer.com"
        e_to: "alerts@mailer.com"
        e_smtp_host: "127.0.0.1"
        e_smtp_port: "25"

    keys/values depend on requirement of each individual
    module - e.g. sensu-mailer.py should specify what
    file to read and what to expect in the config file
    '''

    try:
        with open(filename) as f:
            config = yaml.load(f.read())
    except Exception as e:
        print('Exception: ' + str(e))

    if type(config) is dict:
        if 'settings' not in config.keys():
            print('Error: config file ' + filename + ' does not contain "settings: "')
    else:
        return {}

    return config


def sanitize(data):
    '''santize data/characters from alerts,etc.
    that cannot be parsed as json'''

    replace = {
        '\n': ''
    }

    for key, val in replace.items():
        data = re.sub(key, val, data)

    return data


def checkeventstate(event):
    '''check state of the alert, occurrences, interval,
    refreshes, stashes, etc'''

    defaults = {
        'occurrences': 1,
        'interval': 30,
        'refresh': 600
    }

    if 'occurrences' in event.keys():
        occurrences = event['occurrences']
    else:
        occurrences = defaults['occurrences']

    if 'interval' in event.keys():
        interval = event['check']['interval']
    else:
        interval = defaults['interval']

    if 'refresh' in event.keys():
        refresh = event['check']['refresh']
    else:
        refresh = defaults['refresh']

    if occurrences > defaults['occurrences'] and event['action'] == 'create':
        number = refresh / interval
        if int(number) == 0 or event['occurrences'] % number == 0:
            return True
        else:
            print('INFO: Only handling every __'
                  + str(number) + '__ occurrences')

    return False


def checkstashes(event):
    '''checks sensu stashes, will return False if a stash
    was found so that no alert will be sent'''

    return True
