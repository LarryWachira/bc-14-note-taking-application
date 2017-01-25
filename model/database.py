import sqlite3

conn = sqlite3.connect('PyNote.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS PyNotes
                (Id INTEGER PRIMARY KEY,
                 Note TEXT NOT NULL,
                 Date_Added DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')))''')
conn.commit()

def create_note(note_content):
    conn
    cur.execute('''INSERT INTO PyNotes(Note) VALUES(?)''', [note_content])
    conn.commit()
    conn.close()

def view_note(note_id):
    cur.execute()
    pass

def delete_note(note_id):
    pass

def note_search(query_string):
    pass
