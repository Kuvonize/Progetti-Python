from id3v1 import read_id3v1
from id3v2 import read_id3v2, write_id3v2
import argparse

parser=argparse.ArgumentParser(prog='mp3tag', description="Lettura/scrittura tag MP3 (ID3v1/ID3v2)")
subparsers=parser.add_subparsers(dest='cmd', required=True)

p_read=subparsers.add_parser('read', help='Legge i tag dal file MP3')
p_read.add_argument('file', help='Percorso del file .mp3')

p_write=subparsers.add_parser('write-v2', help='Scrive tag ID3v2 (e copertine)')
p_write.add_argument('file', help='Percorso del file .mp3')
p_write.add_argument("--title")
p_write.add_argument("--artist")
p_write.add_argument("--album")
p_write.add_argument("--album-artist")
p_write.add_argument("--year")
p_write.add_argument("--track")
p_write.add_argument("--track-total")
p_write.add_argument("--genre")
p_write.add_argument("--comment")
p_write.add_argument("--cover", help="Percorso a .jpg/.jpeg/.png")
p_write.add_argument("--no-v23", action="store_true", help="Salva in ID3v2.4 invece di v2.3")

args=parser.parse_args()
if args.cmd=='read':
    path=args.file
    v2=read_id3v2(path)
    v1=read_id3v1(path)

    if v2.get('title'):
        title_v2 = v2['title']
    else:
        title_v2 = "(non presente)"

    if v2.get('artist'):
        artist_v2 = v2['artist']
    else:
        artist_v2 = "(non presente)"

    if v2.get('album'):
        album_v2 = v2['album']
    else:
        album_v2 = "(non presente)"

    if v2.get('album_artist'):
        album_artist_v2 = v2['album_artist']
    else:
        album_artist_v2 = "(non presente)"

    if v2.get('year'):
        year_v2 = v2['year']
    else:
        year_v2 = "(non presente)"

    if v2.get('track'):
        track_v2 = v2['track']
    else:
        track_v2 = "(non presente)"

    if v2.get('genre'):
        genre_v2 = v2['genre']
    else:
        genre_v2 = "(non presente)"

    if v2.get('comment'):
        comment_v2 = v2['comment']
    else:
        comment_v2 = "(non presente)"

    # v2: cover (stringa pronta)
    if v2.get('has_cover'):
        cover_v2 = f"Sì (mime={v2.get('cover_mime')}, size={v2.get('cover_size')} B)"
    else:
        cover_v2 = "No"

    print(f"Titolo: {title_v2}")
    print(f"Artista: {artist_v2}")
    print(f"Album: {album_v2}")
    print(f"Album Artist: {album_artist_v2}")
    print(f"Anno: {year_v2}")
    print(f"Traccia: {track_v2}")
    print(f"Genere: {genre_v2}")
    print(f"Commento: {comment_v2}")
    print(f'Cover: {cover_v2}')

    if v1 is None:
        v1_present = False
    else:
        v1_present = True

    if v1_present and v1.get('title'):
        title_v1 = v1['title']
    else:
        title_v1 = "(non presente)"

    if v1_present and v1.get('artist'):
        artist_v1 = v1['artist']
    else:
        artist_v1 = "(non presente)"

    if v1_present and v1.get('album'):
        album_v1 = v1['album']
    else:
        album_v1 = "(non presente)"

    if v1_present and v1.get('year'):
        year_v1 = v1['year']
    else:
        year_v1 = "(non presente)"

    if v1_present and (v1.get('track') is not None):
        track_v1 = str(v1['track'])
    else:
        track_v1 = "(non presente)"

    # per il genere v1 usa il nome
    if v1_present and v1.get('genre_name'):
        genre_v1 = v1['genre_name']
    else:
        genre_v1 = "(non presente)"

    if v1_present and v1.get('comment'):
        comment_v1 = v1['comment']
    else:
        comment_v1 = "(non presente)"

        
    print(f"Titolo: {title_v1}")
    print(f"Artista: {artist_v1}")
    print(f"Album: {album_v1}")
    print(f"Anno: {year_v1}")
    print(f"Traccia: {track_v1}")
    print(f"Genere: {genre_v1}")
    print(f"Commento: {comment_v1}")           

elif args.cmd == "write-v2":
    path=args.file
    data={}

    if args.title:
        data['title'] = args.title
    if args.artist:
        data['artist'] = args.artist
    if args.album:
        data['album'] = args.album
    if args.genre:
        data['genre'] = args.genre
    if args.comment:
        data['comment'] = args.comment

    if args.album_artist and args.album_artist.strip():
        data['album_artist'] = args.album_artist
    elif args.artist:
        data['album_artist'] = args.artist

    if args.year and len(str(args.year)) == 4 and str(args.year).isdigit():
        data['year'] = str(args.year)

    if args.track is not None:
        data['track'] = args.track
    if args.track_total is not None:
        data['track_total'] = args.track_total

    if args.cover:
        cover_path = args.cover
    else:
        cover_path = None

    if args.no_v23:
        force_v23 = False
    else:
        force_v23 = True

    res=write_id3v2(path=args.file,data=data,cover_path=cover_path,force_v23=force_v23)
    print(f'File: {path}')    
    print(f"Aggiornati: {', '.join(data.keys()) if data else '(nessuno)'}")
    if cover_path:
        if isinstance(res, dict) and res.get('cover_mime') is not None:
            print(f"Cover: aggiunta (mime={res['cover_mime']}, size={res['cover_size']} B)")
        else:
            print("Cover: aggiunta")
    else:
        print("Cover: non aggiunta")

    print(f"Salvato come: {'ID3v2.3' if force_v23 else 'ID3v2.4'}")    