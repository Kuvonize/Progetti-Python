#Mappa dei generi ID3v1 e helper di conversione

DEFAULT_GENRE_INDEX=12
INDEX_TO_GENRE={
    0 :'Blues',
    1 :'Classic Rock',
    2 :'Country',
    3 : 'Dance',
    4 : 'Disco',
    5 : 'Funk',
    6 : 'Grunge',
    7 : 'Hip-Hop',
    8 : 'Jazz',
    9 : 'Metal',
    10 : 'New Age',
    11 : 'Oldies',
    12 : 'Other',
    13 : 'Pop',
    14 : 'R&B',
    15 : 'Rap',
    16 : 'Reggae',
    17 : 'Rock',
    18 : 'Techno',
    19 : 'Industrial',
    20 : 'Soundtrack'
}

GENRE_TO_INDEX={
    'blues':0,
    'classic rock':1,
    'country':2,
    'dance':3,
    'disco':4,
    'funk':5,
    'grunge':6,
    'hip-hop':7,
    'hip hop':7,
    'jazz':8,
    'metal':9,
    'new age':10,
    'oldies':11,
    'other':12,
    'pop':13,
    'r&b':14,
    'rnb':14,
    'rap':15,
    'reggae':16,
    'rock':17,
    'techno':18,
    'electronic':18,
    'industrial':19,
    'soundtrack':20
}

def normalize(text):
    new_str=text.strip().lower().replace('—','-').replace('_','-')
    str_list=new_str.split()
    final_str=' '.join(str_list)
    return final_str

def genre_name_to_index(name):
    if name=='' or name is None:
        return DEFAULT_GENRE_INDEX
    norm_name=normalize(name)
    if norm_name in GENRE_TO_INDEX:
        return GENRE_TO_INDEX[norm_name]
    else:
        return DEFAULT_GENRE_INDEX
    
def genre_index_to_name(index):
    if index is None or index>20 or index<0:
        return INDEX_TO_GENRE[12]
    if index in INDEX_TO_GENRE:
        return INDEX_TO_GENRE[index]
    else:
        return INDEX_TO_GENRE[12]  
