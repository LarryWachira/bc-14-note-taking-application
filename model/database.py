

import sqlite3

conn = sqlite3.connect('PyNote.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS PyNotes
                (Id INTEGER PRIMARY KEY,
                 Note TEXT NOT NULL,
                 Date_Added DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')))''')
conn.commit()

def create_note(note_content):
    cur.execute('''INSERT INTO PyNotes(Note) VALUES(?)''', [note_content])
    conn.commit()

def view_note(note_id):
    if isinstance(note_id, int):
        try:
            cur.execute('''SELECT Id, Note, Date_Added FROM PyNotes WHERE Id = ?''', [note_id])
            note = cur.fetchone()
            print('\n\tNote ID: ' + str(note[0]) + '\n\tDate Added: ' + str(note[2]) + '\n\n\tNote: ' + note[1])
        except TypeError:
            print('Note does not exist. Try a different Id.')
    else: pass

def delete_note(note_id):
    cur.execute('''DELETE FROM PyNotes WHERE Id = ?''', [note_id])
    conn.commit()

def note_search(query_string):
    cur.execute('''SELECT Id, Note, Date_Added FROM PyNotes WHERE Note LIKE ? ''', ['%' + query_string + '%'])
    results = cur.fetchall()

    if len(results) == 0:
        print("No results found.")

    for row in results:
        if len(row) > 0:
            print('\n\tNote ID: ' + str(row[0]) + '\n\tDate Added: ' + str(row[2]) + '\n\tNote: ' + row[1])
