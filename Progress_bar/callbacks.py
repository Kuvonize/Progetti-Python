def on_progress(evento):
    speed=evento.get('speed_mbps',0.0)
    if 'mb_total' in evento and 'percent' in evento:
        eta=evento.get('eta_sec',None)
        if eta is not None:
            print(f"{evento['mb_downloaded']:.1f} MB di {evento['mb_total']:.1f} MB — "
                f"{evento['percent']:.1f}% — {speed:.2f} MB/s — ETA: {eta:.1f}s",
                end="\r", flush=True)
        else:
            print(f"{evento['mb_downloaded']:.1f} MB di {evento['mb_total']:.1f} MB — "
                    f"{evento['percent']:.1f}% — {speed:.2f} MB/s",
                    end="\r", flush=True) 
    else:
         print(
            f"Scaricati {evento['mb_downloaded']:.1f} MB — {speed:.2f} MB/s",
            end="\r", flush=True
        )       

def on_complete(evento):
    if 'mb_total' in evento and 'percent' in evento:
        print(f"{evento['mb_downloaded']:.1f} MB di {evento['mb_total']:.1f} MB — {evento['percent']:.1f}%")
    else:
        print(f"Scaricati {evento['mb_downloaded']:.1f} MB")    
    print('Completato!')
    elapsed=evento.get('elapsed_sec')
    avg_speed=evento.get('avg_speed_mbps')
    if elapsed is not None and avg_speed is not None:
        print(f"Tempo totale: {elapsed:.1f} s — Velocità media: {avg_speed:.2f} MB/s")

def on_error(evento):
    print(f"{evento.get('message','Errore')} {evento.get('detail','')}") 
