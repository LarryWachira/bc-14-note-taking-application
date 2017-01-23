"""
Usage:
    app note create <note_content>
    app note view <note_id>
    app note delete <note_id>
    app note search <query_string>
    app note exit
    app note (-i | --interactive)
    app note (-h | --help)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
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

            print('Invalid Command!')
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
    intro = 'Welcome to my PyNote!'
    prompt = 'Please type a command'
    file = None

    @docopt_cmd
    def do_create(self, arg):
        """Usage: add <note_content>"""
        pass

    @docopt_cmd
    def do_view(self, arg):
        """Usage: view <note_id>"""
        pass

    @docopt_cmd
    def do_delete(self, arg):
        """Usage: delete <note_id>"""
        pass

    @docopt_cmd
    def do_search(self, arg):
        """Usage: search <query_string>"""
        pass
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