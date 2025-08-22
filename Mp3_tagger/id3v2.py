#Gestione ID3v2 con mutagen, inclusa copertina APIC

from mutagen.id3 import ID3, ID3NoHeaderError, TIT2, TPE1, TALB, TPE2, TRCK, TCON, TDRC, TYER, COMM, APIC

def read_id3v2(path):
    try:
        tags=ID3(path)
    except ID3NoHeaderError:
        return {
            'title':None, 
            'artist':None, 
            'album':None, 
            'album_artist':None, 
            'track':None, 
            'genre':None, 
            'year':None, 
            'comment':None, 
            'has_cover':False, 
            'cover_mime':None, 
            'cover_size':None
        }
    title = None
    artist = None
    album = None
    album_artist = None
    track = None
    genre = None
    year = None
    comment = None
    has_cover = False 
    cover_mime = None
    cover_size = None

    frame=tags.get('TIT2')
    if frame and frame.text:
        title=frame.text[0]

    frame=tags.get('TPE1')
    if frame and frame.text:
        artist=frame.text[0]

    frame=tags.get('TALB')
    if frame and frame.text:
        album=frame.text[0]

    frame=tags.get('TPE2')
    if frame and frame.text:
        album_artist=frame.text[0]

    frame=tags.get('TRCK')
    if frame and frame.text:
        track=frame.text[0]

    frame = tags.get('TCON')
    if frame and frame.text:
        genre = frame.text[0]

    frame = tags.get('TDRC')
    if frame and frame.text:
        year=str(frame.text[0])
    else:        
        frame=tags.get('TYER')
        if frame and frame.text:
            year=frame.text[0]

    comms = tags.getall('COMM')
    if comms==[]:
        comment=None
    else:
        chosen=None
        for frame in comms:
            if frame.lang=='eng' and frame.desc=='':
                chosen=frame
                break    
        else:
            chosen=comms[0]
        if chosen.text and chosen.text!=[]:
            comment=chosen.text[0]
        else:
            comment=None
                            
    apics=tags.getall('APIC')
    if not apics:
        has_cover=False
        cover_mime=None
        cover_size=None
    else:
        chosen=None
        for apic in apics:
            if apic.type==3:
                chosen=apic
                break
        if chosen==None:
            chosen=apics[0]
        has_cover=True
        cover_mime=chosen.mime
        cover_size=len(chosen.data)

    return {
        'title':title, 
        'artist':artist, 
        'album':album, 
        'album_artist':album_artist, 
        'track':track, 
        'genre':genre, 
        'year':year, 
        'comment':comment, 
        'has_cover':has_cover, 
        'cover_mime':cover_mime, 
        'cover_size':cover_size
    }    

def write_id3v2(path,data,cover_path=None,  force_v23=True):
    try:
        tags=ID3(path)
    except ID3NoHeaderError:
        tags=ID3()

    cover_mime=None
    cover_size=None

    if data.get('title'):
        tags.delall('TIT2')
        tags.add(TIT2(encoding=3, text=[data['title']]))

    if data.get('artist'):
        tags.delall('TPE1')
        tags.add(TPE1(encoding=3, text=[data['artist']]))

    if data.get('album'):
        tags.delall('TALB')
        tags.add(TALB(encoding=3, text=[data['album']]))

    if data.get('album_artist'):
        tags.delall('TPE2')
        tags.add(TPE2(encoding=3, text=[data['album_artist']]))
    elif data.get('album_artist') is None and data.get('artist'):
        tags.delall('TPE2')
        tags.add(TPE2(encoding=3, text=[data['artist']]))
            

    
    raw_track = data.get('track')
    if raw_track is not None:
        tags.delall('TRCK')
        track_value=str(raw_track)
        tags.add(TRCK(encoding=3, text=[track_value]))

    if data.get('genre'):
        tags.delall('TCON')
        tags.add(TCON(encoding=3, text=[data['genre']]))

    year_val=data.get('year')
    if year_val and len(str(year_val)) == 4 and str(year_val).isdigit():
        tags.delall('TDRC')
        tags.delall('TYER')       
        tags.add(TDRC(encoding=3, text=[str(year_val)]))
        tags.add(TYER(encoding=3, text=[str(year_val)]))

    if data.get('comment'):
        tags.delall('COMM')
        tags.add(COMM(encoding=3, lang='eng', desc='', text=[ data['comment'] ]))

    if cover_path is not None:
        ext=cover_path.lower()
        if ext.endswith('.jpg') or ext.endswith('.jpeg'):
            mime='image/jpeg'
        elif ext.endswith('.png'):
            mime='image/png'
        else:
            mime='image/jpeg'
        with open(cover_path, 'rb') as fh: img_bytes=fh.read()
        tags.delall('APIC')
        tags.add(APIC(encoding=3, mime=mime, type=3, desc='', data=img_bytes))
        cover_mime=mime
        cover_size=len(img_bytes)

    if force_v23:
        tags.save(path, v2_version=3)
    else:
        tags.save(path)

    return {'saved': True, 
            'cover_added': bool(cover_path), 
            'year': year_val,
            'cover_mime':cover_mime,
            'cover_size':cover_size
            }                 




