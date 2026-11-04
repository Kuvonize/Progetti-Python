# E-card Generator

Piccola web app in Flask per creare biglietti d'auguri (e-card): scegli uno sfondo, un font, la dimensione, il colore e l'allineamento, poi scrivi un messaggio o scegli una frase già pronta. L'app genera l'immagine PNG con Pillow e te la fa scaricare.

## Funzionalità

- 5 sfondi e 4 font inclusi
- Testo personalizzato oppure una frase scelta dall'elenco in `app/quotes.json`
- A capo automatico del testo entro i margini, con centratura verticale
- Campi facoltativi "Per:" e "Da:"
- Leggera ombra sotto il testo
- Validazione del form con messaggi di errore (sfondo, font, dimensione tra 12 e 72)
- Anteprima e download dell'immagine generata

## Struttura

```
ecard_generator/
├── run.py              # app Flask: rotte, validazione, generazione dell'immagine
├── app/
│   ├── templates/      # pagine Jinja2 (base, index, create, result)
│   ├── static/         # sfondi, font, CSS
│   └── quotes.json     # frasi pronte
└── generated/          # immagini create (non versionate)
```

## Installazione e avvio

```bash
cd ecard_generator
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env     # poi inserisci una SECRET_KEY casuale nel file .env
python run.py
```

Apri http://127.0.0.1:5000 nel browser.

## Possibili miglioramenti

- Scelta del colore libera, non solo da un elenco
- Anteprima in tempo reale lato client
- Pulizia automatica delle immagini vecchie in `generated/`
