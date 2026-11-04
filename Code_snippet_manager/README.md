# Code Snippet Manager

Applicazione da riga di comando per salvare pezzi di codice (funzioni, classi, query…) e ritrovarli in seguito, organizzati per linguaggio, categoria e tag. Il codice viene mostrato con l'evidenziazione della sintassi.

## Funzionalità

- Aggiunta, modifica ed eliminazione di snippet, con conferma prima di eliminare
- Elenco in tabella con filtri per linguaggio, categoria e preferiti
- Visualizzazione dello snippet con numeri di riga ed evidenziazione della sintassi (Rich)
- Controllo dei duplicati: non si possono avere due snippet con lo stesso titolo nello stesso linguaggio
- Dati salvati in un database SQLite locale (`data/snippets.db`)

## Struttura

Il codice è diviso in livelli, ognuno con un compito preciso:

```
snippet_manager/
├── cli.py         # comandi Typer e output con Rich (interfaccia utente)
├── services.py    # regole e validazione (titolo obbligatorio, duplicati, tag)
├── repository.py  # query SQL (CRUD)
├── db.py          # connessione e creazione della tabella
└── utils.py       # normalizzazione dei tag, timestamp
```

## Installazione

```bash
cd Code_snippet_manager
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

Tutti i comandi si lanciano dalla cartella `Code_snippet_manager`:

```bash
python -m snippet_manager.cli init                  # crea il database
python -m snippet_manager.cli add                   # aggiunge uno snippet (scrivi FINE per terminare il codice)
python -m snippet_manager.cli list                  # elenca tutti gli snippet
python -m snippet_manager.cli list --lang python    # filtra per linguaggio
python -m snippet_manager.cli list --cat utility --fav
python -m snippet_manager.cli show 3                # mostra lo snippet con id 3
python -m snippet_manager.cli edit 3
python -m snippet_manager.cli delete 3
python -m snippet_manager.cli --help
```

## Possibili miglioramenti

- Comando per segnare uno snippet come preferito
- Ricerca testuale nel titolo e nel contenuto
- Esportazione e importazione in JSON
- Test automatici con pytest
