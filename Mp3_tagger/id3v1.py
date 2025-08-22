#Qui c'è la gestione dei tag ID3v1

from utils import clean_text_field, pad_or_trim, int_to_str, safe_year
from genres import genre_index_to_name, genre_name_to_index

ID3V1_SIZE=128

def read_id3v1(path):
    with open(path,'rb') as f:
        f.seek(0,2)
        size=f.tell()
        if size<ID3V1_SIZE:
            return None
        f.seek(size-ID3V1_SIZE,0)
        block=f.read(ID3V1_SIZE)
        if len(block)!=ID3V1_SIZE:
            return None
        if block[0:3]!=b'TAG':
            return None
        
        title_b=block[3:33]
        artist_b=block[33:63]
        album_b=block[63:93]
        year_b=block[93:97]
        comment30=block[97:127]

        if comment30[28]==0:
            track_byte=comment30[29]
            track=track_byte if track_byte !=0 else None
            comment_b=comment30[0:28]
        else:
            track=None
            comment_b=comment30

        title=clean_text_field(title_b)
        artist=clean_text_field(artist_b)
        album=clean_text_field(album_b)
        year=clean_text_field(year_b)
        comment=clean_text_field(comment_b)

        genre_index=block[127]
        genre_name=genre_index_to_name(genre_index)

        return {
            'title':title,
            'artist':artist,
            'album':album,
            'year':year,
            'comment':comment,
            'track':track,
            'genre_index':genre_index,
            'genre_name':genre_name
                }

def write_id3v1(path, data):
    title_b=pad_or_trim(data.get('title',''),30)
    artist_b=pad_or_trim(data.get('artist',''),30)
    album_b=pad_or_trim(data.get('album',''),30)
    year_str=safe_year(data.get('year',''))
    year_b=int_to_str(year_str,4)
    track=data.get('track')
    comment_text=data.get('comment','')

    if isinstance(track,int)  and not isinstance(track,bool) and 1<=track<=255:
        comment28_b=pad_or_trim(comment_text, 28)
        zero_b=bytes(1)
        track_b=bytes([track])
        comment_b=comment28_b+zero_b+track_b
    else:
        comment_b=pad_or_trim(comment_text,30)

    g=data.get('genre',12)
    if isinstance(g,str):
        g=genre_name_to_index(g)
    elif isinstance(g,int) and not isinstance(g,bool):
        if  g < 0 or g >255:
            g=12
    else:
        g=12
    genre_b=bytes([g])
    block=b'TAG'+title_b+artist_b+album_b+year_b+comment_b+genre_b
    if len(block)!=ID3V1_SIZE:
        raise ValueError
    with open(path,'rb+') as f:
        f.seek(0,2)
        size=f.tell()
        if size>=ID3V1_SIZE:
            f.seek(size-ID3V1_SIZE)
            if f.read(3) == b'TAG':
                f.seek(size-ID3V1_SIZE,0)
                f.write(block)
            else:
                f.seek(0,2)
                f.write(block)
        else:
            f.seek(0,2)
            f.write(block)

    return len(block)                    
