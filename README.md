# Progetti Python

Raccolta di progetti che ho scritto per imparare Python: strumenti da riga di comando, una piccola web app in Flask, un compressore con l'algoritmo di Huffman fatto da zero e qualche script di automazione.

Requisiti generali: **Python 3.10+**. I progetti che usano librerie esterne hanno un proprio `requirements.txt`; gli altri usano solo la libreria standard.

## Progetti principali

| Progetto | Cosa fa | Tecnologie |
|---|---|---|
| [Code_snippet_manager](Code_snippet_manager/) | CLI per salvare, cercare e mostrare snippet di codice con evidenziazione della sintassi | Typer, Rich, SQLite |
| [Zip_file_Maker](Zip_file_Maker/) | Crea archivi ZIP con i metodi standard oppure con una **compressione di Huffman scritta a mano** | argparse, zipfile, heapq |
| [ecard_generator](ecard_generator/) | Web app per creare e-card: scegli sfondo, font e testo e scarichi l'immagine | Flask, Pillow |
| [Mp3_tagger](Mp3_tagger/) | Legge e scrive i tag dei file MP3: ID3v1 fatto a mano, ID3v2 con copertina | mutagen, argparse |
| [Sort_Exc_CSV](Sort_Exc_CSV/) | Ordina file CSV/Excel su più colonne, con vari stili di ordinamento | pandas, openpyxl |

## Altri esercizi

| Progetto | Cosa fa |
|---|---|
| [Quiz_maker](Quiz_maker/) | Genera un quiz casuale e il relativo foglio delle risposte da una banca di domande CSV (con convertitore da OpenTDB) |
| [Progress_bar](Progress_bar/) | Scarica un file in un thread separato con barra di avanzamento, pausa, ripresa e annullamento |
| [Site_Checker](Site_Checker/) | Controlla a intervalli regolari se un sito risponde e avvisa a schermo o via email |
| [Mail_checker](Mail_checker/) | Controlla via IMAP se arrivano nuove email non lette su Gmail |
| [Flower_shop](Flower_shop/) | Esercizio di programmazione a oggetti: fiori, bouquet e inventario |
| [Country_from_IP](Country_from_IP/) | Trova il tuo IP pubblico e mostra città, regione e paese |

## Come avviare un progetto

```bash
cd NomeProgetto
python -m venv .venv
.venv\Scripts\activate          # Windows  (su macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt   # solo se il progetto ha un requirements.txt
```

Poi segui le istruzioni nel README del progetto.
