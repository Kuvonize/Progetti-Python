import sqlite3
import pathlib

DB_PATH=pathlib.Path(__file__).resolve().parent.parent/'data'/'snippets.db'
def get_connection():
    con=sqlite3.connect(str(DB_PATH))
    con.row_factory=sqlite3.Row
    return con

def init_db():
    pathlib.Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    con=get_connection()
    cur=con.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            language TEXT,
            category TEXT,
            tags TEXT,
            content TEXT NOT NULL,
            favorite INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
            );
          ''')
    con.commit()
    con.close()