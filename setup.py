#!/usr/bin/env python

import sys, os
from distutils.core import setup
from distutils.command.install_data import install_data

# Pulled from Django setup.py circa django 1.2
class osx_install_data(install_data):
    # On MacOS, the platform-specific lib dir is /System/Library/Framework/Python/.../
    # which is wrong. Python 2.5 supplied with MacOS 10.5 has an Apple-specific fix
    # for this in distutils.command.install_data#306. It fixes install_lib but not
    # install_data, which is why we roll our own install_data class.
 
    def finalize_options(self):
        # By the time finalize_options is called, install.install_lib is set to the
        # fixed directory, so we set the installdir to install_lib. The
        # install_data class uses ('install_data', 'install_dir') instead.
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)
 
if sys.platform == "darwin": 
    cmdclasses = {'install_data': osx_install_data} 
else: 
    cmdclasses = {'install_data': install_data} 

data_files = []
for dirpath, dirnames, filenames in os.walk('gig'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): 
            del dirnames[i]
    if filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(name='Gig',
        version='0.1',
        description='Python project management',
        author='Tom von Schwerdtner',
        author_email='tomvons@gmail.com',
        url='http://www.bitbucket.org/tvon/gig/',
        packages=['gig', 'gig.commands'],
        scripts=['script/gig',],
        cmdclass = cmdclasses,
        data_files=data_files,
        )