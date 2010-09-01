The whole point of gig is to simplify the bootstrapping process for a Django
project.  No thinking about where your settings will go, where your templates
should live, your project structure or any other "paperwork", just a simple way
to get straight to editing your models.py.

To get started just download the code and install it in the usual manner:

    $ sudo python setup.py install

Usage is as simple as:

    $ gig init myproject

That will create a 'myproject' based on gig/templates/django/. Follow the
instructions printed to the screen and you'll have a working Django site up and
ready for development.

Ideally the template would be easily cusotmized, but at the moment it is an
empty, admin-enabled Django site with some basic linuxy configs and HTML5
Boilerplate added.

Notes:

* Need to replace project root through some configs (apache and logrotate.conf).
* User templates
* Some kind of sensible way for variations on a project buildout
