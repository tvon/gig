import os, sys

# TODO: is this a good idea?
sys.stdout = sys.stderr

basedir = '{{ GIG_PROJECT_HOME }}'
sys.path[1:1] = ['%s/config' % basedir, '%s/app' % basedir, '%s/lib' % basedir]

# TODO: This is rather os-dependant
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/egg-cache'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
