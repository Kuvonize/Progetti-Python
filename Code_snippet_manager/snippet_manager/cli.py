import typer
from snippet_manager.db import init_db
from snippet_manager.services import add_snippet,edit_snippet
from snippet_manager.repository import list_snippets, get_snippet_by_id,delete_snippet
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

app=typer.Typer(help='Snippet Manager')

@app.command()
def init():
    init_db()
    print('Database Pronto')

@app.command()
def add():
    title=input('Titolo: ')
    language=input('Linguaggio: ')
    category=input('Categoria: ')
    tags=input('Tag (separati da virgola): ')
    print("Inserisci il codice. Scrivi 'FINE' su una riga vuota per terminare.")
    righe=[]
    while True:
        riga=input()
        if riga.strip()=='FINE':
            break
        righe.append(riga)

    content='\n'.join(righe)

    try:
        new_id=add_snippet(title,language,category,tags,content)
        print(f'Creato snippet con id: {new_id}')
    except ValueError as e:
        print(f'Errore: {e}')

@app.command()
def list(
    lang: str = typer.Option(None, "--lang", help="Filtra per linguaggio"),
    cat: str = typer.Option(None, "--cat", help="Filtra per categoria"),
    fav: bool = typer.Option(False, "--fav", help="Mostra solo preferiti"),
    ):
    rows= list_snippets(language=lang,category=cat,only_fav=fav)
    
    if not rows:
        print('Nessuno snippet trovato.')
        return
    console=Console()
    table=Table(title='Elenco Snippet')
    table.add_column('ID',justify="right", style="cyan", no_wrap=True)
    table.add_column('Titolo',style='magenta')
    table.add_column('Linguaggio',style='green')
    table.add_column('Categoria',style='yellow')
    table.add_column('★', style='bold red', justify='center')  
    table.add_column('Aggiornato',style='white')
    for r in rows:
        id_str = str(r['id'])
        titolo = r['title'] or ''
        lingua = r['language'] or ''
        categoria = r['category'] or ''
        updated = r['updated_at'] or ''
        fav = '★' if r['favorite'] == 1 else ''
        table.add_row(id_str, titolo, lingua, categoria, fav, updated)
    console.print(table)   

@app.command()
def show(id:int):
    row=get_snippet_by_id(id)
    if row is None:
        print('Snippet non trovato')
        return
    console=Console()
    console.print(f"[cyan]ID:[/cyan] {row['id']}")
    console.print(f"[magenta]Titolo:[/magenta] {row['title']}")
    console.print(f"[green]Linguaggio:[/green] {row['language']}")
    console.print(f"[yellow]Categoria:[/yellow] {row['category']}")
    console.print(f"[white]Aggiornato:[/white] {row['updated_at']}")
    console.print(f"[bold red]Preferito:[/bold red] {'★' if row['favorite'] == 1 else ''}")
    console.print(f"[blue]Creato:[/blue] {row['created_at']}")
    console.print(f"[white]Tag:[/white] {row['tags'] or ''}")
    lang = row["language"] or "python"  # fallback
    syntax = Syntax(row["content"], lang, theme="monokai", line_numbers=True)
    console.print(syntax)

@app.command()
def edit(id:int):
    snippet=get_snippet_by_id(id)
    if snippet is None:
        print('Snippet non trovato')
        return
    nuovo_title = None 
    nuovo_lang = None
    nuovo_cat = None
    nuovo_tag = None
    nuovo_content = None
    print(f"TITOLO attuale: {snippet['title'] or ''}")
    i=input('Nuovo Titolo (lascia vuoto e premi invio se non vuoi cambiarlo): ')
    if i.strip():
        nuovo_title=i

    print(f"LINGUAGGIO attuale: {snippet['language'] or ''}")  
    i=input('Nuovo Linguaggio (lascia vuoto e premi invio se non vuoi cambiarlo): ')
    if i.strip():
        nuovo_lang=i

    print(f"CATEGORIA attuale: {snippet['category'] or ''}")
    i=input('Nuova Categoria (lascia vuoto e premi invio se non vuoi cambiarlo): ')
    if i.strip():
        nuovo_cat=i

    print(f"TAG attuali: {snippet['tags'] or ''}")
    i=input('Nuovo Tag (lascia vuoto e premi invio se non vuoi cambiarlo): ')
    if i.strip():
        nuovo_tag=i          

    vuoi_mod=input('Vuoi modificare il contenuto?(s/n): ')
    if vuoi_mod.strip().lower()=='s':
        righe=[]
        print('Scrivi il nuovo contenuto, termina con FINE')
        while True:
            i=input('')
            if i=='FINE':
                break
            righe.append(i)
        if len(righe)==0:
            nuovo_content=None
        else:       
            nuovo_content='\n'.join(righe)

    try:
        righe_mod = edit_snippet(
        id,
        title=nuovo_title,
        language=nuovo_lang,
        category=nuovo_cat,
        tags=nuovo_tag,
        content=nuovo_content
    )
    except ValueError as e:
        print("Errore:", e)
        return      

    if righe_mod>0:
        print('Snippet Aggiornato')
    else:
        print('Nessuna modifica applicata')    

@app.command()
def delete(id:int):
    row=get_snippet_by_id(id)
    if row is None:
        print('Snippet non trovato')
        return
    print(f"ID: {id} - Titolo: {row['title']}")
    risp=input("Confermi l'eliminazione?(s/n): ")
    risp_trimmed=risp.strip().lower()
    if risp_trimmed.startswith('n'):
        print('Annullato')
        return
    elif risp_trimmed.startswith('s'):
        rows_deleted=delete_snippet(id)
        if rows_deleted>0:
            print('Eliminato')
            return
        else:
            print('Nessuna riga è stata eliminata')
            return  
    else:
        print('Risposta non valida. Annullato')
        return    

          




if __name__=='__main__':
    app()