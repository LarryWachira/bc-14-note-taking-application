

"""
Usage:
    PyNote create <note_content>...
    PyNote view <note_id>
    PyNote delete <note_id>
    PyNote search <query_string>...
    PyNote list --limit [<items_per_page>]
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
    intro = '\n\t\t\t\tWelcome to PyNote!\n\t    -Type help for a list for instructions on how to use the app.'
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
        note_id = num_check(arg)

        if isinstance(note_id, int):
            print('\nAre you sure you want to delete:')
            view_note(note_id)
            answer = input("Type yes to confirm or anything else to abort > ")
            if answer == 'yes' or answer == 'YES' or answer == 'Yes':
                delete_note(note_id)
                print('Note deleted!')
            else:
                print('Operation Cancelled!')

    @docopt_cmd
    def do_search(self, args):
        """Usage: search <query_string>..."""
        query_string = query_to_string(args)
        note_search(query_string)

    # def do_divided_search(self, args):
    #     """Usage: search <query_string>..."""
    #     query_string = query_to_string(args)
    #     note_search(query_string)

    @docopt_cmd
    def do_list(self, arg):
        """Usage: list --limit [<items_per_page>]"""
        if arg['<items_per_page>'] is None:
            note_list()
        else:
            items_per_page = num_check_limit(arg)
            narrowed_lists(items_per_page)

    @docopt_cmd
    def do_import_export(self, arg):
        """Usage: list"""
        pass

    @docopt_cmd
    def do_help(self, arg):
        """Usage: help"""
        print('''
      \t\t\t\t   Commands:
      \t   create <note_content>...       |  Creates a new note
      \t   view <note_id>                 |  Views the note that has the given Id
      \t   delete <note_id>               |  Deletes the note that has the given Id
      \t   search <query_string>...       |  Searches all notes that have the given keyword
      \t   list [--limit <items_per_page>]|  Lists all stored notes
      \t   help                           |  Help instructions

      \t-Words enclosed in guillemetes '< >' should guide you on the required number
      \t of arguments, except when they appear like this: '< >...' when any number
      \t of arguments is allowed.
      \t-Square brackets '[]' denote optional arguments.
      \t-Separate different arguments with a space.

                           ||Type exit to close the app||''')

    def do_exit(self, arg):
        """Exits Interactive Mode."""
        close_db()
        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    try:
        print(__doc__)
        PyNote().cmdloop()
    except KeyboardInterrupt:
        print("Exiting App")