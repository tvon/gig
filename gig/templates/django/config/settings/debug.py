import sys, os, platform

print "======================================================================"
print "__name__ =", __name__
print "__file__ =", __file__
print "os.getpid() =", os.getpid()
print "os.getcwd() =", os.getcwd()
print "os.curdir =", os.curdir
print "sys.path =", repr(sys.path)
print "sys.modules.keys() =", repr(sys.modules.keys())

# Of course this makes no sense since we don't have the typical 'mysite' setup
print "sys.modules.has_key('mysite') =", sys.modules.has_key('mysite')
if sys.modules.has_key('mysite'):
    print "sys.modules['mysite'].__name__ =", sys.modules['mysite'].__name__
    print "sys.modules['mysite'].__file__ =", sys.modules['mysite'].__file__

print "os.environ['DJANGO_SETTINGS_MODULE'] =", os.environ.get('DJANGO_SETTINGS_MODULE', None)
print "platform.node() =", platform.node()
print "======================================================================"
