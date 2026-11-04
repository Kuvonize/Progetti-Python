# Zip File Maker

Strumento da riga di comando che crea archivi ZIP da file e cartelle. Offre due modalità:

- **builtin**: usa la libreria standard `zipfile` con i metodi `store`, `deflate`, `bzip2` o `lzma`;
- **huffman**: comprime ogni file con una **codifica di Huffman implementata da zero** e la salva nello ZIP insieme a un `MANIFEST.json`. Questa modalità serve a scopo didattico.

## Come funziona la compressione di Huffman

In [`compressors/huffman.py`](compressors/huffman.py):

1. **Tabella delle frequenze**: conta quante volte compare ognuno dei 256 valori di byte.
2. **Albero di Huffman**: usa una coda di priorità (`heapq`), con un contatore per decidere i casi di parità, e unisce di volta in volta i due nodi meno frequenti.
3. **Tabella dei codici**: visita l'albero; i byte più frequenti ottengono i codici più corti. Il caso con un solo simbolo è gestito a parte.
4. **Codifica**: impacchetta i bit in byte, con il padding sull'ultimo byte.
5. **Serializzazione**: scrive un header con le 256 frequenze, la dimensione originale e il numero di bit, seguito dai dati compressi (`struct`, little-endian).

Ogni file finisce nello ZIP come `nome.huf`. Il `MANIFEST.json` riporta per ogni file la dimensione originale e quella compressa.

## Uso

Non servono librerie esterne. Dalla cartella `Zip_file_Maker`:

```bash
# ZIP standard (deflate, livello 6)
python cli.py documenti/ -o out/archivio.zip --recursive

# metodo e livello a scelta, escludendo alcuni file
python cli.py src/ -o out/src.zip --recursive --method lzma --level 9 --exclude "*.log" --exclude "*.tmp"

# percorsi interni relativi a una cartella base
python cli.py progetto/ -o out/p.zip --recursive --base progetto

# compressione di Huffman
python cli.py testo.txt -o out/huffman.zip --algo huffman
```

Alla fine stampa un riepilogo: numero di file, dimensione in ingresso e dimensione dello ZIP.

## Possibili miglioramenti

- Decompressore per i file `.huf`, con un test che verifichi che comprimere e poi decomprimere restituisca i dati originali
- Header più compatto: salvare solo le frequenze diverse da zero
