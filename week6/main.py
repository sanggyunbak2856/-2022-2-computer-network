import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
conn = sqlite3.connect('answer.db', check_same_thread=False)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Paste (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 content TEXT);''')
conn.commit()

class Paste(BaseModel):
    content: str

@app.get('/')
def root():
    return {'message': 'Hello world'}

@app.get('/paste/{paste_id}')
def get_paste(paste_id: int):
    res = cur.execute('''SELECT id, content
                      FROM Paste
                      WHERE id = ?''', (paste_id, ))
    data = res.fetchone()
    if data is not None:
        paste = Paste(content = data[1])
        return {
            'paste_id' : data[0],
            'paste' : paste
        }
    else:
        return {
            'paste_id' : paste_id,
            'paste' : None
        }

@app.post('/paste/')
def post_paste(paste: Paste):
    cur.execute('''INSERT INTO Paste (content) VALUES(?)''', (paste.content, ))
    conn.commit()
    

@app.put('/paste/{paste_id}')
def put_paste(paste_id: int, paste: Paste):
    cur.execute('''UPDATE Paste SET content = ? WHERE id = ?''', (paste.content, paste_id))
    conn.commit()

@app.delete('/paste/{paste_id}')
def delete_paste(paste_id: int):
    cur.execute('''DELETE FROM Paste WHERE id = ?''', (paste_id, ))
    conn.commit()