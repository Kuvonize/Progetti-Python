import threading
from downloader import scarica


class DownloadWorker:
    def __init__(self,url,destinazione,on_progress,on_complete,on_error):
        self.url = url
        self.destinazione = destinazione
        self.on_progress = on_progress
        self.on_complete = on_complete
        self.on_error = on_error
        self._thread = None
        self.pause_event=threading.Event()
        self.stop_event=threading.Event()

    def _run(self):
        try:
            scarica(self.url,self.destinazione,self.on_progress,self.on_complete,self.on_error,pause_event=self.pause_event,stop_event=self.stop_event)
        except Exception as e:
            evento={
                    'type':'error',
                    'message':'Errore imprevisto',
                    'detail':str(e)
                    }  
            if self.on_error:
                self.on_error(evento)

    def start(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def join(self,timeout=None):
        if self._thread:
            self._thread.join(timeout)

    def is_alive(self):
        if self._thread:
            return self._thread.is_alive()
        else:
            return False  

    def pause(self):
        self.pause_event.set()

    def resume(self):
        self.pause_event.clear() 

    def stop(self):
        self.stop_event.set()



