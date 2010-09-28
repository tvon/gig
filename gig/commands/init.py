import sys
import os
import re
import shutil
import stat
from optparse import make_option

import gig
from gig.utils import _make_writeable
from gig.base import BaseCommand, LabelCommand, CommandError


def copy_helper(template_dir, dest, name, omit=[]):
    """
    Copies a `template_dir` directory tree to `dest`/`name`
    
    Eg, if template is 'django', it copies the template directory named 'django' to '%s/%s/' % (dest, name)
    """
    # name -- The name of the application or project.
    
    # directory -- The directory to which the layout template should be copied.
    # other_name -- When copying an application layout, this should be the name
    #               of the project.
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

            # Ignore dummy files (used to have empty directories in hg/git) and anything we're omitting
            if f in ['.empty'] + omit:
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
        for template in templates:
            try:
                # XXX Kinda messy...
                newpath = os.path.join(self.template_dir, template)
                sys.path.append(newpath)
                
                import gighooks
                
                print '%s - %s' % (template, gighooks.name)
                print '\t', gighooks.description
                
                # restore sys.path
                sys.path = sys.path[:-1]
                
                # XXX: is this the right way to do this?
                # delete import reference 
                del gighooks
                
            except:
                print template

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
        
        template_path = os.path.join(self.template_dir, self.template)
        target_path = os.path.abspath(name)
        copy_helper(template_path, target_path, name, omit=['gighooks.py',])

        # Adding our template to the path so we can import gighooks.
        # Honestly not sure this is the best way to do it, but....
        sys.path.append(template_path)

        try:
            import gighooks
            
            # XXX Should error check the existance of these things
            gighooks.post_build(target_path)
            # Other info to pass here?
            print "\n"
            print gighooks.notes % {'target_path': target_path}
        except ImportError:
            print "No setup hooks found, template build assumed to be complate."