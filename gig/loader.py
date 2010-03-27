"""
95% of this was proudly and shamelessly borrowed from Django.

Notes:

    * Need a way to list installed package and do wholesale system upgrades.
    * Ability to instally install to sandbox.
    * No support for eggs until I can get an understaning of why they are necessary
"""
import os
import sys
from optparse import OptionParser, NO_DEFAULT

import gig
from gig.base import BaseCommand, handle_default_options

_commands = None

def load_command_class(mod_name, name):
    """
    Given a command name and an module name, returns the Command class
    instance. All errors raised by the import process (ImportError,
    AttributeError) are allowed to propagate.
    """
    module = import_module('%s.%s' % (mod_name, name))
    return module.Command()


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]

def find_commands(command_dir):
    """
    Given a path to a command directory, returns a list of all the command
    names that are available.

    Returns an empty list if no commands are defined.
    """
    try:
        return [f[:-3] for f in os.listdir(command_dir) if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []


def get_commands():
    """
    Returns a dictionary mapping command names to their callback applications.

    This works by looking for a management.commands package in django.core, and
    in each installed application -- if a commands package exists, all commands
    in that package are registered.

    Core commands are always included. If a settings module has been specified,
    user-defined commands will also be included, the startproject command will
    be disabled, and the startapp command will be modified to use the directory
    in which the settings module appears.

    The dictionary is in the format {command_name: app_name}. Key-value pairs
    from this dictionary can then be used in calls to
    load_command_class(app_name, command_name)

    If a specific version of a command must be loaded (e.g., with the startapp
    command), the instantiated module can be placed in the dictionary in place
    of the application name.

    The dictionary is cached on the first call and reused on subsequent calls.
    """
    global _commands

    if _commands is None:
        core_commands_dir = '%s/commands/' % gig.__path__[0]
#        _commands = dict([(name, 'gig.projects') for name in find_commands('%s/projects/commands/' % gig.__path__[0])])
        _commands = dict([(name, 'gig.commands') for name in find_commands(core_commands_dir)])

    return _commands


class LaxOptionParser(OptionParser):
    """
    An option parser that doesn't raise any errors on unknown options.

    This is needed because the --pythonpath option affects the commands (and
    thus the options) that are available to the user.
    """
    def error(self, msg):
        pass

    def print_help(self):
        """Output nothing.

        The lax options are included in the normal option parser, so under
        normal usage, we don't need to print the lax options.
        """
        pass

    def print_lax_help(self):
        """Output the basic options available to every command.

        This just redirects to the default print_help() behaviour.
        """
        OptionParser.print_help(self)

    def _process_args(self, largs, rargs, values):
        """
        Overrides OptionParser._process_args to exclusively handle default
        options and ignore args and other options.

        This overrides the behavior of the super class, which stop parsing
        at the first unrecognized option.
        """
        while rargs:
            arg = rargs[0]
            try:
                if arg[0:2] == "--" and len(arg) > 2:
                    # process a single long option (possibly with value(s))
                    # the superclass code pops the arg off rargs
                    self._process_long_opt(rargs, values)
                elif arg[:1] == "-" and len(arg) > 1:
                    # process a cluster of short options (possibly with
                    # value(s) for the last one only)
                    # the superclass code pops the arg off rargs
                    self._process_short_opts(rargs, values)
                else:
                    # it's either a non-default option or an arg
                    # either way, add it to the args list so we can keep
                    # dealing with options
                    del rargs[0]
                    raise Exception
            except:
                largs.append(arg)


class ManagementUtility(object):
    """
    Encapsulates the logic of the gig command running.

    A ManagementUtility has a number of commands, which can be manipulated
    by editing the self.commands dictionary.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])

    def main_help_text(self):
        """
        Returns the script's main help text, as a string.
        """
        usage = ['',"Type '%s help <subcommand>' for help on a specific subcommand." % self.prog_name,'']
        usage.append('Available subcommands:')
        commands = get_commands().keys()
        commands.sort()
        for cmd in commands:
            usage.append('  %s' % cmd)
        return '\n'.join(usage)

    def fetch_command(self, subcommand):
        """
        Tries to fetch the given subcommand, printing a message with the
        appropriate command called from the command line if it can't be found.
        """
        try:
            app_name = get_commands()[subcommand]
            if isinstance(app_name, BaseCommand):
                # If the command is already loaded, use it directly.
                klass = app_name
            else:
                klass = load_command_class(app_name, subcommand)
        except KeyError:
            sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n" % \
                (subcommand, self.prog_name))
            sys.exit(1)
        return klass

    def execute(self):
        """
        Given the command-line arguments, this figures out which subcommand is
        being run, creates a parser appropriate to that command, and runs it.
        """
        # Preprocess options to extract --pythonpath.  These options could
        # affect the commands that are available, so they must be processed
        # early.
        parser = LaxOptionParser(usage="%prog subcommand [options] [args]",
                                 version=gig.get_version(),
                                 option_list=BaseCommand.option_list)
                                 
        options, args = parser.parse_args(self.argv)
        handle_default_options(options)
         
        try:
            options, args = parser.parse_args(self.argv)
            handle_default_options(options)
        except:
            print "EXCEPTION DAMMIT"
            pass # Ignore any option errors at this point.

        try:
            subcommand = self.argv[1]
        except IndexError:
            sys.stderr.write("Type '%s help' for usage.\n" % self.prog_name)
            sys.exit(1)

        if subcommand == 'help':
            if len(args) > 2:
                self.fetch_command(args[2]).print_help(self.prog_name, args[2])
            else:
                parser.print_lax_help()
                sys.stderr.write(self.main_help_text() + '\n')
                sys.exit(1)

        # Special-cases: We want 'gig --version' and 'gig --help' to work, for
        # backwards compatibility.
        elif self.argv[1:] == ['--version']:
            # LaxOptionParser already takes care of printing the version.
            pass
        elif self.argv[1:] == ['--help']:
            parser.print_lax_help()
            sys.stderr.write(self.main_help_text() + '\n')
        else:
            self.fetch_command(subcommand).run_from_argv(self.argv)


def execute_manager(argv=None):
    """
    A simple method that runs a ManagementUtility
    """
    utility = ManagementUtility(argv)
    utility.execute()

