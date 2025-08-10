import csv
import random
import pathlib
from datetime import date




def genera_quiz(banca_domande, numero_domande):
    domande_scelte=random.sample(banca_domande,numero_domande)
    quiz_finale=[]
    chiave_correzione={}
    for domanda in domande_scelte:
        id_domanda=domanda['id']
        testo=domanda['testo']
        opzioni_lista=domanda['opzioni'].split('|')
        if len(opzioni_lista)==4:
            corretta=opzioni_lista[0]
            random.shuffle(opzioni_lista)
            indice_corretta=opzioni_lista.index(corretta)
            lettere = ["A", "B", "C", "D"]
            lettera_corretta=lettere[indice_corretta]
            chiave_correzione[id_domanda]=lettera_corretta
            struttura_finale={'id':id_domanda,
                            'testo':testo,
                            'opzioni':opzioni_lista
                            }
            quiz_finale.append(struttura_finale)
        else:
            continue
    return quiz_finale, chiave_correzione    
    
def scrivi_quiz(percorso,quiz_finale,nome_studente,data):
    pathlib.Path(percorso).parent.mkdir(parents=True,exist_ok=True)
    with open(percorso,'w',encoding='utf-8') as file:
        file.write('QUIZ\n')
        file.write(f'Studente: {nome_studente}\n')
        file.write(f'Data: {data}\n\n')
        letters=['A','B','C','D']
        n=1
        for domanda in quiz_finale:
            testo=domanda['testo']
            opzioni=domanda['opzioni']
            file.write(f'{n}) {testo}\n')
            for i in range(4):
                file.write(f'{letters[i]} {opzioni[i]}\n')
            file.write('\n')
            n+=1    

def scrivi_chiave(percorso, chiave_correzione):
    lista=['id','corretta']
    pathlib.Path(percorso).parent.mkdir(parents=True, exist_ok=True)
    with open(percorso,'w',encoding='utf-8',newline='') as file:
        writer=csv.DictWriter(file, fieldnames=lista, extrasaction="ignore", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for id_domanda, lettera in chiave_correzione.items():
            writer.writerow({'id':id_domanda,
                             'corretta':lettera})
    return len(sorted(chiave_correzione))

def carica_banca_domande(percorso_csv):
    if pathlib.Path(percorso_csv).is_file():
        with open(percorso_csv,'r',encoding='utf-8') as file:
            domande=[]
            for riga in csv.DictReader(file):
                domande.append(riga)
    else:
        raise RuntimeError(f'File non trovato: {percorso_csv}')
    
    
    return domande
