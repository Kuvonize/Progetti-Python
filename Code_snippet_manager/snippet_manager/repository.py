from snippet_manager.db import get_connection

def create_snippet(data):
    con=get_connection()
    cur=con.cursor()
    cur.execute('INSERT INTO snippets(title, language, category, tags, content, favorite, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?)',
                (data["title"], data["language"], data["category"], data["tags"], data["content"], data["favorite"], data["created_at"], data["updated_at"]))
    con.commit()
    new_id=cur.lastrowid
    con.close()
    return new_id

def exists_same_title_lang(title,language):
    con=get_connection()
    cur=con.cursor()
    query='SELECT 1 FROM snippets WHERE title = ? AND language = ? LIMIT 1;'
    cur.execute(query, (title, language))
    row=cur.fetchone()
    con.close()
    return row is not None

def list_snippets(language=None, category=None, only_fav=False):
    con=get_connection()
    cur=con.cursor()
    query='SELECT id, title, language, category, favorite, updated_at FROM snippets'
    conditions=[]
    params=[]
    if language is not None and language!='':
        conditions.append('language=?')
        params.append(language.lower()) 
    if category is not None and category!='':
        conditions.append('category=?')
        params.append(category.lower()) 
    if only_fav==True:
        conditions.append('favorite=1')

    if len(conditions) > 0:
        query+=' WHERE ' + ' AND '.join(conditions)
    
    query+=' ORDER BY updated_at DESC'    
    cur.execute(query,params)
    rows=cur.fetchall()
    con.close()

    return rows

def get_snippet_by_id(id:int):
    query='SELECT * FROM snippets WHERE id=?'
    con=get_connection()
    cur=con.cursor()
    cur.execute(query,(id,))
    row=cur.fetchone()
    con.close()

    return row

def update_snippet(id:int,data:dict):
    if not data:
        return 0
    con=get_connection()
    cur=con.cursor()

    set_parts=[]
    params=[]

    for (chiave,valore) in data.items():
        if chiave in ("title","language","category","tags","content","favorite","created_at","updated_at"):
            set_parts.append(f'{chiave}=?')
            params.append(valore)
    if len(set_parts)==0:
        return 0             
    query='UPDATE snippets SET ' + ', '.join(set_parts) + ' WHERE id=?'
    params.append(id)
    cur.execute(query,params)
    con.commit()
    righe_modificate=cur.rowcount
    con.close()

    if not righe_modificate:
        return 0
    
    return righe_modificate

def delete_snippet(id):
    con=get_connection()
    cur=con.cursor()
    query='DELETE FROM snippets WHERE id=?'
    cur.execute(query,(id,))
    con.commit()
    row=cur.rowcount
    con.close()
    return row
