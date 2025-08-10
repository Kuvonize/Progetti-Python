import json
import csv
import html
import pathlib
import re
INPUT_JSON="domande/opentdb_50.json"
OUTPUT_CSV="domande/banca_domande.csv"
def pulisci_testo(testo):
    pulito=html.unescape(testo)
    testo_pulito=pulito.replace('|','/').replace('\n',' ').replace('\r',' ').replace('\t',' ')
    pattern=r"\s+"
    testo_pulito=re.sub(pattern,' ',testo_pulito)
    testo_pulito=testo_pulito.strip()
    return testo_pulito

def carica_domande_da_json(percorso):
    with open(percorso,'r',encoding="utf-8") as dati:
        contenuto=json.load(dati)
        if not ('results' in contenuto and isinstance(contenuto['results'], list)):
            raise RuntimeError("Formato Json inatteso: chiave 'results' mancante o non in lista")
        else:
            return contenuto['results']

def trasforma(records_json):
    righe=[]
    for i,record in enumerate(records_json,start=1):
        if record['type']!='multiple':
            continue
        testo=record['question']
        correct_answer=record['correct_answer']
        incorrect_answers=record['incorrect_answers']
        argomento=record['category']
        difficolta=record['difficulty']
        if (not isinstance(incorrect_answers, list)) or (not len(incorrect_answers)==3):
            continue
        testo_pulito=pulisci_testo(testo)
        corretta_pulita=pulisci_testo(correct_answer)
        sbagliate_pulite=[]
        for answer in record['incorrect_answers']:
            risposta_pulita=pulisci_testo(answer)
            sbagliate_pulite.append(risposta_pulita)
        tutte_le_opzioni=[corretta_pulita]+sbagliate_pulite    
        opzioni='|'.join(tutte_le_opzioni)
        id_string=str(i)
        id_num=id_string.zfill(3)
        id='Q'+id_num
        domanda = {
            "id": id,
        "testo": testo_pulito,
        "opzioni": opzioni,
        "corretta": "A",          # la giusta è la prima
        "difficolta": difficolta,
        "argomento": argomento,
        "punti": 1
        }
        righe.append(domanda)

    return righe       

def scrivi_csv(percorso,righe):
    lista_colonne=['id','testo','opzioni','corretta','difficolta','argomento','punti']
    pathlib.Path(percorso).parent.mkdir(parents=True,exist_ok=True)
    with open(percorso,'w',encoding='utf-8',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=lista_colonne,extrasaction='ignore',quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(righe)

    return len(righe)    

def main():
    dati=carica_domande_da_json(INPUT_JSON)
    righe=trasforma(dati)
    if not righe:
       print('Nessuna domanda valida trovata')
    else:
        n=scrivi_csv(OUTPUT_CSV,righe)
        print(f"Conversione completata: {n} domande salvate in '{OUTPUT_CSV}'.")

if __name__=='__main__':
    main()