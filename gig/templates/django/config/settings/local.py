from base import *

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
