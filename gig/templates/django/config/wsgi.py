import os, sys

PROJECT_HOME = os.path.dirname(os.path.abspath('%s/../' % __file__))
sys.path[1:1] = ['%s/config' % PROJECT_HOME, '%s/app' % PROJECT_HOME, '%s/lib' % PROJECT_HOME]

# TODO: is this a good idea?
sys.stdout = sys.stderr

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