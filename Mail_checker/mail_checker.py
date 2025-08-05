import imaplib
import time
import email
from email.utils import parsedate_to_datetime
import getpass

user=input('Inserisci la mail che vuoi controllare (deve essere gmail!): ')
password=getpass.getpass('Inserisci la password (servirà una password app, se non ne sei in possesso vai qui https://myaccount.google.com/apppasswords): ')
try:
    with open("id_letti.txt", "r") as f:
        id_precedenti = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    id_precedenti = set()
imap_obj=imaplib.IMAP4_SSL('imap.gmail.com',993)
imap_obj.login(user,password)
check=True
timer=int(input('Ogni quanto devo eseguire di nuovo il controllo?: '))

while check==True:
    lista_email=[]
       
    imap_obj.select(mailbox='INBOX', readonly=True)
    status, ids_bytes=imap_obj.search(None,'UNSEEN')
    ids_decoded=ids_bytes[0].decode("utf-8")
    ids_list=ids_decoded.split()
    ids_attuali=set(ids_list)
    nuovi_ids=ids_attuali-id_precedenti

    for id in nuovi_ids:
        status, fetch_data=imap_obj.fetch(id,'RFC822')
        if status != 'OK' or not fetch_data or not fetch_data[0]:
            print(f"Errore nel recupero della mail con ID: {id}")
            continue
        raw_email=fetch_data[0][1]
        mail=email.message_from_bytes(raw_email)
        raw_data=mail.get('Date')
        mail_date=parsedate_to_datetime(raw_data)
        lista_email.append((id,mail_date))

    lista_email.sort(key=lambda x: x[1])
    for id, data in lista_email:
        print(f"Nuova email ricevuta - ID: {id}, Data: {data}")

    id_precedenti=ids_attuali
    with open("id_letti.txt", "w") as f:
        for id in id_precedenti:
            f.write(f"{id}\n")
    while True:
        x=input('Desideri che il mail checker rimanga attivo?(si/no): ')
        if x[0].lower()=='s':
            print('Continuo a rimanere in ascolto!')
            check=True
            break
        elif x[0].lower()=='n':
            print('Mi fermo qui allora!')
            check=False
            break
        else:
            print('Scelta errata!')    
    time.sleep(timer)

imap_obj.logout()