#!/usr/bin/env python
import sys

PROJECT_HOME = os.path.dirname(os.path.abspath('%s/../' % __file__))
sys.path[1:1] = ['%s/config' % PROJECT_HOME, '%s/app' % PROJECT_HOME, '%s/lib' % PROJECT_HOME]

from django.core.management import setup_environ

try:
    from settings import settings
    setup_environ(settings)
except ImportError:
    import sys
    sys.stderr.write("Error: Can't import settings")
    sys.exit(1)

#
# Put cron commands here
#
