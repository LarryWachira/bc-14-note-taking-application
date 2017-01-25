"""
Usage:
    PyNote create <note_content>...
    PyNote view <note_id>
    PyNote delete <note_id>
    PyNote search <query_string>
    PyNote list
    PyNote help
    PyNote (-i | --interactive)
    PyNote (-h | --help)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    type exit to close the app
"""

import cmd
import datetime
import sys
import time
from docopt import docopt, DocoptExit
from controller.functions import *
from model.database import *


# from functions import *


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.

            print('\nInvalid Command! Also check the number of arguments that can be passed in \'Usage:\' below.')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class PyNote(cmd.Cmd):
    intro = 'Welcome to PyNote!'
    prompt = '\nPlease type a command >> '
    file = None
    ts = time.time()
    date_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    @docopt_cmd
    def do_create(self, args):
        """Usage: create <note_content>..."""
        note_content = list_to_string(args)
        create_note(note_content)
        print('\n\t\''+ note_content + '\'' + ' | note has been created.\n\t Timestamp | ' + self.date_time)

    @docopt_cmd
    def do_view(self, arg):
        """Usage: view <note_id>"""
        note_id = num_check(arg)
        view_note(note_id)

    @docopt_cmd
    def do_delete(self, arg):
        """Usage: delete <note_id>"""
        pass

    @docopt_cmd
    def do_search(self, arg):
        """Usage: search <query_string>"""
        pass

    @docopt_cmd
    def do_help(self, arg):
        """Usage: help"""
        print('''
    Usage:
    \tPyNote create <note_content>...
    \tPyNote view <note_id>
    \tPyNote delete <note_id>
    \tPyNote search <query_string>
    \tPyNote list
    \tPyNote help
    \n\tWords ecnclosed in guillemetes '< >' should guide you on the acceptable number of arguments,
    \texcept when they appear like this: '< >...' when any number of arguments is allowed.

                                       ||type exit to close the app||'''
    )

    def do_exit(self, arg):
        """Exits Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    try:
        print(__doc__)
        PyNote().cmdloop()
    except KeyboardInterrupt:
        print("Exiting App")