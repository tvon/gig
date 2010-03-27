import sys
import platform

production = ('app.example.com',)

hostname = platform.node().split('.')[0].replace('-', '_')

try:
    # If basic hosntame, unmodified, is in production list:
    if platform.node() in production:
        print >> sys.stderr, "Importing settings from: production (host %s)" % platform.node()
        settings = __import__('production', globals(), locals(), [], -1) 
    else:
        try:
            settings = __import__(hostname, globals(), locals(), [], -1)
            print >> sys.stderr, "Importing settings from: %s" % hostname
        except ImportError:
            settings = __import__('local', globals(), locals(), [], -1)
            print >> sys.stderr, "Importing settings from: local"
except ImportError:
    print >> sys.stderr, "Unable to import host-specific settings module '%s', falling back to 'base'" % hostname
    import base as settings
