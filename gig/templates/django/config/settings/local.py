from base import *

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'devel.db',
    }
}

MEDIA_URL = '/static/'

MEDIA_ROOT = '%s/media/' % PROJECT_HOME

TEMPLATE_DIRS = (
    '%s/templates/' % PROJECT_HOME,
)

# django-debug-toolbar setup
INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.extend([
    'debug_toolbar'
])

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
MIDDLEWARE_CLASSES.extend([
    'debug_toolbar.middleware.DebugToolbarMiddleware',
])

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}