

import sqlite3
import json
from firebase import firebase
import requests


class NotesDatabase:

    def __init__(self):
        conn = sqlite3.connect('PyNote.db')
        self.conn = conn
        cur = conn.cursor()
        self.cur = cur

        cur.execute('''CREATE TABLE IF NOT EXISTS PyNotes
                    (Id INTEGER PRIMARY KEY,
                    Note TEXT NOT NULL,
                    Date_Added DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')))''')

    def create_note(self, note_content):

        self.cur.execute('''INSERT INTO PyNotes(Note) VALUES(?)''', [note_content])
        self.conn.commit()

    def view_note(self, note_id):

        if isinstance(note_id, int):
            try:
                self.cur.execute('''SELECT * FROM PyNotes WHERE Id = ?''', [note_id])
                note = self.cur.fetchone()
                print('\n\tNote ID: ' + str(note[0]) + '\n\tDate Added: ' + str(note[2]) + '\n\n\tNote: ' + note[1])
            except TypeError:
                print('\n\tNote Id does not exist. Try a different Id.')
        else:
            pass

    def delete_note(self, note_id):

        self.cur.execute('''DELETE FROM PyNotes WHERE Id = ?''', [note_id])
        self.conn.commit()

    def note_search(self, query_string):

        self.cur.execute('''SELECT * FROM PyNotes WHERE Note LIKE ? ''', ['%' + query_string + '%'])
        results_note = self.cur.fetchall()

        self.cur.execute('''SELECT * FROM PyNotes WHERE Id LIKE ? ''', ['%' + query_string + '%'])
        results_id = self.cur.fetchall()

        if len(results_note) == 0 and len(results_id) == 0:
            print("\n\tNo results found.")

        for row in results_note:
            if len(row) > 0:
                print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])

        for row in results_id:
            if len(row) > 0:
                print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])

    def paginated_search(self, query_string, items_per_page):

        if isinstance(items_per_page, int):

            self.cur.execute('''SELECT Note FROM PyNotes
                        WHERE Note LIKE ?''',
                        ('%' + query_string + '%',))
            results_all = self.cur.fetchall()

            self.cur.execute('''SELECT * FROM PyNotes
                        WHERE Note LIKE ? LIMIT ? ''',
                        ('%' + query_string + '%', items_per_page))
            results = self.cur.fetchall()

            if len(results_all) == 0:
                print('\n\tNo results found.')

            elif len(results_all) > 0:
                for row in results:
                    print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])

                new_offset = items_per_page
                count = len(results_all)

                while new_offset < (count + 1):
                    response = input('\nType N to go to Next Page or Q to quit > ')

                    if response == 'N' or response == 'n':
                        self.cur.execute('''SELECT Id, Note, Date_Added FROM PyNotes
                                    WHERE Note LIKE ? LIMIT ? OFFSET ?''',
                                    ('%' + query_string + '%', items_per_page, new_offset))
                        results = self.cur.fetchall()

                        for row in results:
                            print('\n\tNote ID: ' + str(row[0]) +
                                  '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])

                        new_offset += items_per_page

                    elif response == 'Q' or response == 'q':
                        break

                    else:
                        print('\n\tInvalid Input')
                    continue

                print('\n\tEnd of notes.')

        else:
            pass

    def note_list(self):

        self.cur.execute('''SELECT * FROM PyNotes''')
        results = self.cur.fetchall()

        for row in results:
            print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])

    def paginated_list(self, items_per_page):

        if isinstance(items_per_page, int):
            self.cur.execute('''SELECT * FROM PyNotes LIMIT ? ''', [items_per_page])
            results = self.cur.fetchall()

            for row in results:
                print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])

            self.cur.execute('''SELECT COUNT(Note) FROM PyNotes''')
            result = self.cur.fetchone()

            num_of_rows = result[0]
            new_offset = items_per_page

            while new_offset < (num_of_rows + 1):
                response = input('\nType N to go to Next Page or Q to quit > ')

                if response == 'N' or response == 'n':
                    self.cur.execute('''SELECT * FROM PyNotes LIMIT ? OFFSET ?''',(items_per_page, new_offset))
                    results = self.cur.fetchall()

                    for row in results:
                        print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])

                    new_offset += items_per_page

                elif response == 'Q' or response == 'q':
                    break

                else:
                    print('Invalid Input')
                continue

            print('\n\tEnd of notes.')

        else:
            pass

    def export_json(self):
        self.cur.execute('''SELECT * FROM PyNotes''')
        database = self.cur.fetchall()
        data = json.dumps(database)

        answer = input('\n\tWould you like to export your notes to a database.json file?\n\nType yes or no: ')
        if answer == 'YES' or answer == 'yes' or answer == 'y' or answer == 'Yes':
            file = open('database.json', 'w')
            file.write(data)
            file.close()
            print('\n\tNotes export complete. You can find the file in the app directory.')

        elif answer == 'NO' or answer == 'no' or answer == 'n' or answer == 'No':
            print('\n\tExport operation aborted.')

        else:
            print('\n\tInvalid input.')

    def import_json(self):
        answer = input('\n\tWould you like to import notes from your back up file?\n\nType yes or no: ')

        if answer == 'YES' or answer == 'yes' or answer == 'y' or answer == 'Yes':
            try:
                file = open('database.json', 'r')
                data = file.read()
                file.close()
                rows = json.loads(data)

                for row in rows:
                    self.cur.execute('''INSERT INTO
                                      PyNotes(Id, Note, Date_Added) VALUES(?, ?, ?)''', (row[0], row[1], row[2]))
                    self.conn.commit()

                print('\n\tImport completed successfully.')
            except FileNotFoundError:
                print('\n\tBackup file not found.')

        elif answer == 'NO' or answer == 'no' or answer == 'n' or answer == 'No':
            print('\n\tImport operation aborted.')

        else:
            print('\n\tInvalid input.')

    def sync(self):

        try:
            response = requests.get("https://pynote-536fd.firebaseio.com/")

            if response.status_code == 200:
                answer = input('\n\tWould you like to sync your notes to firebase?\n\nType yes or no: ')

                if answer == 'YES' or answer == 'yes' or answer == 'y' or answer == 'Yes':
                    self.cur.execute('''SELECT * FROM PyNotes''')
                    data = self.cur.fetchall()
                    fbase = firebase.FirebaseApplication('https://pynote-536fd.firebaseio.com/')
                    result = fbase.post('/db', json.dumps(data))
                    print('\n\tSync successful.\n\tSync snapshot: ', result)

                elif answer == 'NO' or answer == 'no' or answer == 'n' or answer == 'No':
                    print('\n\tSync aborted.')

                else:
                    print('\n\tInvalid input.')

            else:
                print('\n\tServer Unavailable.')

        except:
            print('\n\tAn error occurred.')

    def close_db(self):
        self.conn.close()
