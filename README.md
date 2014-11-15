sensu-utils
===========

Sensu handlers, etc. primarily written in python as current sensu-util scripts/handlers are all ruby and require a "modern" ruby which is not that easy on CentOS/RHEL based systems.

HANDLERS
--------

``sensu-mailer.py``
-------------------
- uses sensu-mailer.yaml which needs to be placed into /etc/sensu/conf.d/sensu-mailer.yaml


NOTES and HACKS
---------------
- sensuutils.py needs to be copied into /usr/lib/python*/site-packages/

