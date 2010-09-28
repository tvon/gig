import imp
import os
import tempfile
import urllib2


class IllegalPathError(Exception):
    """Raised when a path we're trying to access is outside of the project tree."""
    pass
    

class Directory(object):
    """A project directory, used to niceify the template interface
    """
    
    def __init__(self, path, newdir=None):
        """How to make sure all created directories are within project home?"""
        fullpath = os.path.abspath('%s/%s' % (path, newdir))
        
        self.checkpath(path, fullpath)
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)
        self.path = fullpath
        
    def mkdir(self, path):
        """
        Create a directory under the project directory, return a Directory() 
        of the newly created directory
        """
        fullpath = '%s/%s' % (self.path, path)
        
        # Make sure fullpath is under self.path
        self.checkpath(self.path, fullpath)
        
        os.mkdir(fullpath)
        return Directory(self.path, path)
        
    def mkfile(self, name, contents=''):
        """Create a file with specified contents (or empty)"""
        f = open('%s/%s' % (self.path, name), 'w')
        f.write(contents)
        f.close()
    
    def checkpath(self, base, new):
        """Make sure 'new' relative path is within 'base' path
        """
        if not new.startswith(base):
            raise IllegalPathError('Directory is outside of the project path')


class Template(object):

    def __init__(self, url):
        suffix = ('.py', 'U', 1) # Need to educate self on this...
        
        fd, filename = tempfile.mkstemp(suffix='.py', text=True)
        f = os.fdopen(fd, "w")
        
        try:
            f.write( urllib2.urlopen(url).read() )
            f.flush()

            # XXX: I don't really understand why I need to re-open, just passing the above 
            # fdopen()'d file does not work
            self.script = imp.load_module(url, open(filename), filename, suffix)
            
        finally:
            f.close()

    def setup(self, *args, **kwargs):
        return self.script.setup(*args, **kwargs)
        
    @property
    def requirements(self):
        if hasattr(self.script, 'requirements'):
            return self.script.requirements
        else:
            return False
            
        
class Project(Directory):
    
    def __init__(self, destdir, name, scripturl=None):
        self.name = name
        self.destdir = destdir
        self.scripturl = scripturl
        self.template = Template(scripturl)
        Directory.__init__(self, destdir, name)
        
    def setup(self):
        """
        Pass a Directory object to the template setup() function so the template 
        can build out our project
        """
        return self.template.setup(Directory(self.destdir, self.name))
        
    def handle_requirements(self):
        if self.template.requirements:
            self.mkfile('requirements.txt', self.template.requirements)

            if False: # if self.is_virtualenv:
                self.pipinstall()
        
    def pipinstall(self):
        """
        if file_exists requirements.txt and in_virtualenv:
            exec "pip install -r requirements.txt" # but only show errors
        else:
            notice-when-done "the file requirements.txt contains required files, run pip install -r requirements.txt..."
        """
        pass
    
    def virtualenv(self):
        """
        if not in_virtualenv and make_virtualenv_option:
            mkvirtualenv 'projectname'
        """
        pass