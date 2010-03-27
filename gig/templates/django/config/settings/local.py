from base import *

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'devel.db'

MEDIA_URL = '/static/'

MEDIA_ROOT = '%s/media/' % PROJECT_HOME

TEMPLATE_DIRS = (
    '%s/templates/' % PROJECT_HOME,
)
