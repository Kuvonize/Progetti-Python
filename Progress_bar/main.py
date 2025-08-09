from download_worker import DownloadWorker
from callbacks import on_complete,on_progress,on_error
from queue import Queue,Empty
import time
import threading

#url per le prove: https://proof.ovh.net/files/1Gb.dat

if __name__ == "__main__":
    url = input("Inserisci l'url del file da scaricare: ")
    destinazione = input('Inserisci il percorso di dove vuoi salvare il file: ')
    q=Queue()
    def enqueue_progress(evento): q.put(evento)
    def enqueue_complete(evento): q.put(evento)
    def enqueue_error(evento): q.put(evento)
    worker=DownloadWorker(url,destinazione,enqueue_progress,enqueue_complete,enqueue_error)
    print('Download avviato...')
    worker.start()
    def _command_loop():
        print('[p]=pausa / [r]=riprendi / [c]=annulla (invio dopo la lettera)')
        while worker.is_alive():
            try:
                cmd=input().strip().lower()
            except EOFError:
                break
            if cmd=='p':
                worker.pause()
            elif cmd=='r':
                worker.resume()
            elif cmd=='c':
                worker.stop()
                break

    t_cmd=threading.Thread(target=_command_loop,daemon=True)
    t_cmd.start()                    
    
    try:
        while True:
            try:
                evento=q.get(timeout=0.1)
            except Empty:
                if not worker.is_alive():
                    break
                continue        
                
            if evento['type']=='progress':
                on_progress(evento)
            elif evento['type']=='complete':
                on_complete(evento)
                break
            elif evento['type']=='cancelled':
                print("Download annullato dall'utente")
                break
            elif evento['type']=='error':
                on_error(evento)
                break
    except KeyboardInterrupt:
        on_error({'type':'error','message':'Interrotto dall’utente','detail':''})            
    finally:
        print()        
        worker.join() 
    


