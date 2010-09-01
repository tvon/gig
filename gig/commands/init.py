import sys
import os
import re
from ConfigParser import ConfigParser
from optparse import make_option

import gig
from gig.base import BaseCommand, LabelCommand, CommandError


def copy_helper(template_dir, dest, name):
    # app_or_project, name, directory, template,other_name=''):
    """
    Copies a `template_dir` directory tree to `dest`/`name`
    
    Eg, if template is 'django', it copies the template directory named 'django' to '%s/%s/' % (dest, name)
    """
    # name -- The name of the application or project.
    
    # directory -- The directory to which the layout template should be copied.
    # other_name -- When copying an application layout, this should be the name
    #               of the project.
    import re
    import shutil
    if not re.search(r'^[_a-zA-Z-]\w*$', name): # If it's not a valid directory name.
        # Provide a smart error message, depending on the error.
        if not re.search(r'^[_a-zA-Z-]', name):
            message = 'make sure the name begins with a letter or underscore'
        else:
            message = 'use only numbers, letters, underscores and hyphens'
        raise CommandError("%r is not a valid project name. Please %s." % (name, message))

    top_dir = os.path.abspath(dest)
    try:
        os.mkdir(top_dir)
    except OSError, e:
        raise CommandError(e)

    # TODO: Not platform friednly, or well done...
    template = os.path.split(template_dir)[1]

    for d, subdirs, files in os.walk(template_dir):
        relative_dir = d[len(template_dir)+1:].replace(template, name)
        if relative_dir:
            print "\tdir:\t%s/" % os.path.join(name, relative_dir)
            os.mkdir(os.path.join(top_dir, relative_dir))

        # Ignore 'hidden' directories
        for i, subdir in enumerate(subdirs):
            if subdir.startswith('.'):
                del subdirs[i]

        for f in files:

            # A dummy file so we can have empty directories in git/hg
            if f == '.empty':
                continue

            path_old = os.path.join(d, f)
            path_new = os.path.join(top_dir, relative_dir, f.replace(template, name))
            fp_old = open(path_old, 'r')
            fp_new = open(path_new, 'w')
            print "\tfile:\t%s" % os.path.join(name, relative_dir, f.replace(template, name))
            fp_new.write(fp_old.read().replace('{{ GIG_PROJECT_NAME }}', name).replace('{{ GIG_PROJECT_HOME }}', dest))
            fp_old.close()
            fp_new.close()
            try:
                shutil.copymode(path_old, path_new)
                _make_writeable(path_new)
            except OSError:
                sys.stderr.write("Notice: Couldn't set permission bits on %s. You're probably using an uncommon filesystem setup. No problem.\n" % path_new)

def _make_writeable(filename):
    """ 
    Make sure that the file is writeable. Useful if our source is
    read-only.
    """
    import stat
    if sys.platform.startswith('java'):
        # On Jython there is no os.access()
        return
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)


class Command(BaseCommand):

    help = 'initialize new project'
    args = '[project_name]'

    option_list = BaseCommand.option_list + (
        make_option('-l', '--list', help='List available project templates', action='store_true'),
        make_option('-t', '--template', help='Template to use, defaults to "django"'),
    )

    template_dir = '%s/templates/' % gig.__path__[0]
    template = 'django'

    def get_templates(self):
        # TODO: Make this better...
        templates = os.listdir(self.template_dir)
        return templates

    def handle_list(self):
        templates = self.get_templates()
        for t in templates:
            print t

    def handle(self, *args, **options):

        if options.get('list') == True:
            self.handle_list()
            sys.exit(0)

        if options.get('template'):
            self.template = options.get('template')

        if len(args) < 1:
            sys.stderr.write('You must provide a destination project name\n')
            sys.exit(1)

        # Make sure it exists...
        if not os.path.exists(self.template_dir + self.template):
            sys.stdout.write('Template for "%s" not found, please specify another template.\n' % self.template)
            sys.exit(1)

        name = args[0]
        copy_helper(os.path.join(self.template_dir, self.template), os.path.abspath(name), name)

        gigrc = os.path.join(self.template_dir, self.template, '.gigrc')
        gigrc_defaults = {'gig_project_home': os.path.abspath(name), 'gig_project_name': name}
        if os.path.exists(gigrc):
            config = ConfigParser(gigrc_defaults)
            config.read(gigrc)
            if config.has_section('Template Data'):
                if config.has_option('Template Data', 'post_install_notes'):
                    notes = config.get('Template Data', 'post_install_notes')
                    print ''
                    for line in notes.split('\n'):
                        print re.sub(r'^\|', '', line)
                    print ''
        else:
            print "Does Not Exist: %s" % os.path.join(self.template_dir, self.template, '.gigrc')
