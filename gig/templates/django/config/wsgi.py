import os, sys

# TODO: is this a good idea?
sys.stdout = sys.stderr

basedir = '{{ GIG_PROJECT_HOME }}'

for dir in ['config', 'app', 'lib']:
    sys.path.insert(0, '%s/%s' % (basedir, dir))

# This gives us the proper hostname settings config
from settings import settings

import django.core.management
django.core.management.setup_environ(settings)
utility = django.core.management.ManagementUtility()
command = utility.fetch_command('runserver')

command.validate()

import django.conf
import django.utils

django.utils.translation.activate(django.conf.settings.LANGUAGE_CODE)

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()