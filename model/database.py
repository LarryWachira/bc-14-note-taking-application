

import sqlite3
import json
from firebase import firebase
import requests

conn = sqlite3.connect('PyNote.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS PyNotes
            (Id INTEGER PRIMARY KEY,
            Note TEXT NOT NULL,
            Date_Added DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')))''')


def create_note(note_content):
    cur.execute('''INSERT INTO PyNotes(Note) VALUES(?)''', [note_content])
    conn.commit()


def view_note(note_id):

    if isinstance(note_id, int):
        try:
            cur.execute('''SELECT * FROM PyNotes WHERE Id = ?''', [note_id])
            note = cur.fetchone()
            print('\n\tNote ID: ' + str(note[0]) + '\n\tDate Added: ' + str(note[2]) + '\n\n\tNote: ' + note[1])
        except TypeError:
            print('Note does not exist. Try a different Id.')
    else:
        pass


def delete_note(note_id):

    cur.execute('''DELETE FROM PyNotes WHERE Id = ?''', [note_id])
    conn.commit()


def note_search(query_string):

    cur.execute('''SELECT * FROM PyNotes WHERE Note LIKE ? ''', ['%' + query_string + '%'])
    results_note = cur.fetchall()

    cur.execute('''SELECT * FROM PyNotes WHERE Id LIKE ? ''', ['%' + query_string + '%'])
    results_id = cur.fetchall()

    if len(results_note) == 0 and len(results_id) == 0:
        print("\n\tNo results found.")

    for row in results_note:
        if len(row) > 0:
            print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])

    for row in results_id:
        if len(row) > 0:
            print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])


def paginated_search(query_string, items_per_page):

    if isinstance(items_per_page, int):

        cur.execute('''SELECT Note FROM PyNotes
                    WHERE Note LIKE ?''',
                    ('%' + query_string + '%',))
        results_all = cur.fetchall()

        cur.execute('''SELECT * FROM PyNotes
                    WHERE Note LIKE ? LIMIT ? ''',
                    ('%' + query_string + '%', items_per_page))
        results = cur.fetchall()

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
                    cur.execute('''SELECT Id, Note, Date_Added FROM PyNotes
                                WHERE Note LIKE ? LIMIT ? OFFSET ?''',
                                ('%' + query_string + '%', items_per_page, new_offset))
                    results = cur.fetchall()

                    for row in results:
                        print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])

                    new_offset += items_per_page

                elif response == 'Q' or response == 'q':
                    break

                else:
                    print('\n\tInvalid Input')
                continue

            print('\n\tEnd of notes.')

    else:
        pass


def note_list():

    cur.execute('''SELECT * FROM PyNotes''')
    results = cur.fetchall()

    for row in results:
        print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])


def paginated_list(items_per_page):

    if isinstance(items_per_page, int):
        cur.execute('''SELECT * FROM PyNotes LIMIT ? ''', [items_per_page])
        results = cur.fetchall()

        for row in results:
            print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])

        cur.execute('''SELECT COUNT(Note) FROM PyNotes''')
        result = cur.fetchone()

        num_of_rows = result[0]
        new_offset = items_per_page

        while new_offset < (num_of_rows + 1):
            response = input('\nType N to go to Next Page or Q to quit > ')

            if response == 'N' or response == 'n':
                cur.execute('''SELECT Id, Note, Date_Added FROM PyNotes LIMIT ? OFFSET ?''',(items_per_page, new_offset))
                results = cur.fetchall()

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


def export_json():
    cur.execute('''SELECT * FROM PyNotes''')
    database = cur.fetchall()
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


def import_json():
    answer = input('\n\tWould you like to import notes from your back up file?\n\nType yes or no: ')

    if answer == 'YES' or answer == 'yes' or answer == 'y' or answer == 'Yes':
        try:
            file = open('database.json', 'r')
            data = file.read()
            file.close()
            rows = json.loads(data)

            for row in rows:
                cur.execute('''INSERT INTO PyNotes(Id, Note, Date_Added) VALUES(?, ?, ?)''', (row[0], row[1], row[2]))
                conn.commit()

            print('\n\tImport completed successfully.')
        except FileNotFoundError:
            print('\n\tBackup file not found.')

    elif answer == 'NO' or answer == 'no' or answer == 'n' or answer == 'No':
        print('\n\tImport operation aborted.')

    else:
        print('\n\tInvalid input.')


def sync():
    try:
        response = requests.get("https://pynote-536fd.firebaseio.com/")
        if response.status_code == 200:
            answer = input('\n\tWould you like to sync your notes to firebase?\n\nType yes or no: ')

            if answer == 'YES' or answer == 'yes' or answer == 'y' or answer == 'Yes':
                cur.execute('''SELECT * FROM PyNotes''')
                data = cur.fetchall()
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
        print('\n\tError occurred.')


def close_db():
    conn.close()
