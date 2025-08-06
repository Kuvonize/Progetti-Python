import time
import requests
import smtplib
from email.message import EmailMessage
import getpass

site=input('Inserisci url o IP del sito o server che vuoi controllare: ')
interval=int(input("Inserisci l'intervallo di secondi che occore tra un controllo e l'altro: "))
notification_method=input('Dove vuoi ricevere la notifica?(mail o a schermo?): ')
while True:
    if notification_method[0].lower()=='m':
        display=False
        mail=True
        indirizzo_mail=input('A quale indirizzo vuoi ricevere le notifiche?: ')
        try:
            psw=getpass.getpass('Inserisci la password (servirà una password app, se non ne sei in possesso vai qui https://myaccount.google.com/apppasswords): ')
            break
        except Exception:
            psw=input('Inserisci la password (servirà una password app, se non ne sei in possesso vai qui https://myaccount.google.com/apppasswords): ')
            break
    elif notification_method[0].lower()=='s':
        mail=False
        display=True
        break
    else:
        print('Scelta errata!')        

sito_giu=False  

def invia_mail(mittente, destinatario, psw, tipo_errore, dettaglio):
    oggetto = 'ALLERTA: sito offline!'
    corpo = f"{tipo_errore}: {dettaglio}"

    msg = EmailMessage()
    msg["From"] = mittente
    msg["To"] = destinatario
    msg["Subject"] = oggetto
    msg.set_content(corpo)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(mittente, psw)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as errore_mail:
        print(f"Errore nell'invio della mail: {errore_mail}")
        return False

while True:
    try:
        response = requests.get(site,timeout=10)
        if response.status_code == 200:
            sito_giu = False
            stato = f'[{time.ctime()}] Sito Online!'
            print(stato)
            with open('monitoraggio.log', 'a', encoding="utf-8") as log:
                log.write(stato + '\n')

        else:
            stato = f"[{time.ctime()}] Errore HTTP: {response.status_code} {response.reason}"

            if display:
                print(stato)

            if mail and not sito_giu:
                if invia_mail(indirizzo_mail, indirizzo_mail, psw, "Errore HTTP", f"{response.status_code} {response.reason}"):
                    sito_giu = True

            with open("monitoraggio.log", "a", encoding="utf-8") as log:
                log.write(stato + "\n")

    except requests.exceptions.RequestException as errore:
        stato = f"[{time.ctime()}] Sito giù, errore: {str(errore)}"
        print(stato)

        with open("monitoraggio.log", "a") as log:
            log.write(stato + "\n")

        if display:
            print(f'ATTENZIONE: il sito è giù \ncodice errore: {str(errore)}')

        if mail and not sito_giu:
            if invia_mail(indirizzo_mail, indirizzo_mail, psw, "Errore di connessione", str(errore)):
                sito_giu = True

    time.sleep(interval)

