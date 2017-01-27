

"""
Usage:
    PyNote create <note_content>...
    PyNote view <note_id>
    PyNote delete <note_id>
    PyNote search <query_string>... [--limit=N]
    PyNote list [--limit=N]
    PyNote sync
    PyNote import
    PyNote export
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
from pyfiglet import Figlet


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
    intro = '\n\t\t\t\tWelcome to PyNote!\n\t    -Type help for a list of instructions on how to use the app-'
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
            print('\n  Are you sure you want to delete:')
            view_note(note_id)
            answer = input("\n  Type yes to confirm or anything else to abort > ")

            if answer == 'yes' or answer == 'YES' or answer == 'Yes':
                delete_note(note_id)
                print('\n\tNote deleted!')
            else:
                print('\n\tOperation Cancelled!')

    @docopt_cmd
    def do_search(self, args):
        """Usage: search <query_string>... [--limit=N]"""
        query_string = query_to_string(args)
        items_per_page = num_check_limit(args)

        if args['--limit'] is not None:
            paginated_search(query_string, items_per_page)

        elif args['--limit'] is None:
            note_search(query_string)

        else:
            pass

    @docopt_cmd
    def do_list(self, arg):
        """Usage: list [--limit=N]"""
        if arg['--limit'] is None:
            note_list()
        else:
            items_per_page = num_check_limit(arg)
            paginated_list(items_per_page)

    @docopt_cmd
    def do_export(self, arg):
        """Usage: export"""
        export_json()

    @docopt_cmd
    def do_import(self, arg):
        """Usage: import"""
        import_json()

    @docopt_cmd
    def do_sync(self, arg):
        """Usage: sync"""
        sync()

    @docopt_cmd
    def do_help(self, arg):
        """Usage: help"""
        print('''
      \t\t\t\t   Commands:
      \t   create <note_content>...                        |  Creates a new note
      \t   view <note_id>                                  |  Views the note that has the given Id
      \t   delete <note_id>                                |  Deletes the note that has the given Id
      \t   search <query_string> --limit [<items_per_page>]|  Searches all notes that have the given keyword
      \t   list [--limit <items_per_page>]                 |  Lists all stored notes
      \t   help                                            |  Help instructions

      \t-Words enclosed in guillemetes '< >' should guide you on the required number
      \t of arguments, except when they appear like this: '< >...' when any number
      \t of arguments is allowed.
      \t-Square brackets '[]' denote optional arguments.
      \t-Separate different arguments with a space.

                           ||Type exit to close the app||''')

    def do_exit(self, arg):
        """Us"""
        close_db()
        print('\n' + '*' * 50 + '\n')
        print('\tThank you for using PyNote!\n')
        print('*'*50)
        f = Figlet(font='slant')
        print(f.renderText('Good Bye!'))
        exit()


opt = docopt(__doc__, sys.argv[1:])


if opt['--interactive']:
    try:
        print('\n'*3)
        f = Figlet(font='block')
        print(f.renderText('PyNote'))
        print('*' * 60)
        print(__doc__)
        PyNote().cmdloop()
    except KeyboardInterrupt:
        print("\n\tExiting App")
