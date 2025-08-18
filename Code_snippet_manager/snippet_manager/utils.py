import datetime

def normalize_tags(s):
    s_pulita=[tag.strip() for tag in s.lower().split(',') if tag.strip()]
    stringa_finale=','.join(s_pulita)
    return stringa_finale

def now_iso():
    tempo=datetime.datetime.now().replace(microsecond=0)
    tempo=tempo.isoformat()

    return tempo
    


