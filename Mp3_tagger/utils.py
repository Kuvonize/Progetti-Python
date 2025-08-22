#Contiene utility comuni per stringhe e campi ID3v1
import re


def pad_or_trim(text,length):
    
    if text==None:
        text=''
    buf=text.encode('latin-1','ignore')
    if len(buf)>length:
        buf=buf[:length] 
    if len(buf)<length:
        pad_len=length-len(buf)
        buf=buf+bytes(pad_len)    
    return buf

def clean_text_field(raw_bytes):
    if raw_bytes is None:
        return ''
    text_dec=raw_bytes.decode('latin-1').rstrip('\x00 ').strip()
    return text_dec

def int_to_str(n,length):
    s=str(n)
    digits=re.sub(r'[^0-9]+','',s) or '0'
    digits=digits[:length]
    b=digits.encode('latin-1')
    if len(b)<length:
        b=b+bytes(length-len(b))
    return b    


def safe_year(value):
    if isinstance(value,int):
        s=str(value)
        return s if re.fullmatch(r'[0-9]{4}', s) else '0000'
    if isinstance(value, str):
        m=re.search(r'[0-9]{4}',value)
        year=m.group(0) if m else '0000'
        return year

    return '0000'    