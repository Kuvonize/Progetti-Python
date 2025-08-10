from quiz_maker import carica_banca_domande, genera_quiz, scrivi_quiz, scrivi_chiave
from datetime import date
from pathlib import Path

PERCORSO_BANCA = Path("domande/banca_domande.csv")
CARTELLA_OUTPUT = Path("output")

def main():
    # 1) input utente
    studente = input("Come ti chiami?: ").strip()
    num_domande = int(input("Quante domande vuoi?: ").strip())

    # 2) carica banca
    banca = carica_banca_domande(PERCORSO_BANCA)
    if num_domande > len(banca):
        print(f"Numero richiesto troppo alto. Max disponibile: {len(banca)}")
        return

    # 3) genera quiz + chiave
    quiz_finale, chiave = genera_quiz(banca, num_domande)

    # 4) nomi file di output
    nome_base = studente.replace(" ", "_")
    data_oggi = date.today().isoformat()
    CARTELLA_OUTPUT.mkdir(parents=True, exist_ok=True)
    percorso_quiz = CARTELLA_OUTPUT / f"quiz_{nome_base}_{data_oggi}.txt"
    percorso_chiave = CARTELLA_OUTPUT / f"chiave_{nome_base}_{data_oggi}.csv"

    # 5) scrivi file
    scrivi_quiz(percorso_quiz, quiz_finale, studente, date.today())
    scrivi_chiave(percorso_chiave, chiave)

    # 6) riepilogo
    print(f"Quiz salvato in: {percorso_quiz}")
    print(f"Chiave salvata in: {percorso_chiave}")
    print(f"Domande generate: {len(quiz_finale)}")

if __name__ == "__main__":
    main()

