import re
import os
from random import choice

name = 'Django project template'
description = 'A basic Django project buildout with a few nicities.'

notes = """
*** Install django-debug-toolbar and django-extensions ***

Run syncdb and you should be good to go with an admin
interface and an otherwise empty site.

If you're content with a user/pass of admin/admin, run this:

    cd %(target_path)s && \\
        script/manage.py syncdb --noinput && \\
        script/manage.py loaddata fixtures/initial.json

Now start the server

    script/manage.py runserver

"""

def post_build(path):
    """Set a secret key"""
    main_settings_file = os.path.join(path, 'config', 'settings', 'base.py')
    settings_contents = open(main_settings_file, 'r').read()
    fp = open(main_settings_file, 'w')
    secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    settings_contents = re.sub(r"(?<=SECRET_KEY = ')'", secret_key + "'", settings_contents)
    fp.write(settings_contents)
    fp.close()
