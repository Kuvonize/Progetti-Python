import requests
import time

def scarica(url,destinazione,on_progress=None,on_complete=None,on_error=None,pause_event=None,stop_event=None):
    try:
        response=requests.get(url,stream=True,timeout=(5,30))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        evento={'type':'error',
                'message':'Errore HTTP!'
                }
        evento['detail']=str(e)
        if on_error:
            on_error(evento)
        return    

    total_bytes=(response.headers.get('Content-Length'))
    if total_bytes is not None:
        total_bytes=int(total_bytes)

    bytes_scaricati=0
    ultimo_stamp=time.monotonic()
    
    with open(destinazione,'wb') as file:
        if stop_event and stop_event.is_set():
            evento={'type':'cancelled',
                    'message':'Annullato da utente',
                    'bytes_downloaded':bytes_scaricati
                    }
            if on_error:
                on_error(evento)
            return
        start_time=time.monotonic()     
        for chunk in response.iter_content(chunk_size=128*1024):
            if stop_event and stop_event.is_set():
                evento = {
                    'type': 'cancelled',
                    'message': 'Annullato da utente',
                    'bytes_downloaded': bytes_scaricati
                }
                if on_error:
                    on_error(evento)
                return    
            if pause_event and pause_event.is_set():
                while pause_event.is_set():
                    if stop_event and stop_event.is_set():
                        evento = {
                             'type': 'cancelled',
                             'message': 'Annullato da utente',
                             'bytes_downloaded': bytes_scaricati
                         }
                        if on_error:
                            on_error(evento)
                        return
                    time.sleep(0.05)                 

            if chunk:
                file.write(chunk)
                bytes_scaricati+=len(chunk)
                if time.monotonic()-ultimo_stamp>=0.1:
                    mb_scaricati=bytes_scaricati/(1024*1024)
                    evento={'type':'progress',
                            'bytes_downloaded':bytes_scaricati,
                            'total_bytes':total_bytes,
                            'mb_downloaded':mb_scaricati
                            }
                    elapsed=time.monotonic()-start_time
                    speed_mbps=(mb_scaricati/elapsed) if elapsed > 0 else 0.0
                    evento['speed_mbps']=speed_mbps
                    if total_bytes is not None and speed_mbps > 0:
                        remaining_mb=(total_bytes-bytes_scaricati)/(1024*1024)
                        evento['eta_sec']=remaining_mb/speed_mbps
                    

                    
                    if total_bytes is not None:
                        mb_totali=total_bytes/(1024*1024)
                        percentuale=bytes_scaricati/total_bytes*100
                        evento['mb_total']=mb_totali
                        evento['percent']=percentuale
                    if on_progress:
                        on_progress(evento)
                    ultimo_stamp=time.monotonic()            
        mb_scaricati = bytes_scaricati / (1024*1024)
        elapsed_total=time.monotonic()-start_time
        evento['elapsed_sec']=elapsed_total
        if elapsed_total>0:
            evento['avg_speed_mbps']=mb_scaricati/elapsed_total
        evento={'type':'complete',
                'bytes_downloaded':bytes_scaricati,
                'total_bytes':total_bytes,
                'mb_downloaded':mb_scaricati
                }
        if total_bytes is not None:
            mb_totali=total_bytes/(1024*1024)
            evento['mb_total']=mb_totali
            evento['percent']=100.0


        if on_complete:
            on_complete(evento)    
        



