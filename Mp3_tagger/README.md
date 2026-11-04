# MP3 Tagger

Strumento da riga di comando per leggere e modificare i metadati (tag) dei file MP3.

- **ID3v1**: lettura e scrittura **implementate a mano** sul blocco di 128 byte alla fine del file: titolo, artista, album, anno, commento, traccia (ID3v1.1) e genere, convertito tra indice e nome.
- **ID3v2**: lettura e scrittura con la libreria `mutagen`, compresa la **copertina** (frame APIC, JPEG o PNG). Si può salvare in ID3v2.3, il formato più compatibile, oppure in v2.4.

## Installazione

```bash
cd Mp3_tagger
pip install -r requirements.txt
```

## Uso

```bash
# legge i tag ID3v2 e ID3v1
python cli.py read "canzone.mp3"

# scrive i tag ID3v2
python cli.py write-v2 "canzone.mp3" --title "Titolo" --artist "Artista" --album "Album" --year 2024 --track 3 --genre Rock

# aggiunge una copertina e salva in ID3v2.4
python cli.py write-v2 "canzone.mp3" --cover copertina.jpg --no-v23
```

Se non indichi `--album-artist`, viene usato lo stesso valore di `--artist`. L'anno viene scritto solo se è composto da 4 cifre.

> Nel repository non ci sono file MP3 di esempio, per motivi di copyright: usa un tuo file per le prove.

## Possibili miglioramenti

- Comando `write-v1` nel CLI: la funzione `write_id3v1` esiste già in `id3v1.py`
- Modifica di più file in una volta (un'intera cartella)
