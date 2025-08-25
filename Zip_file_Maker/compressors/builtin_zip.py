import zipfile
import logging
from pathlib import Path

METHODS={
    'store':zipfile.ZIP_STORED,
    'deflate':zipfile.ZIP_DEFLATED,
    'bzip2':zipfile.ZIP_BZIP2,
    'lzma':zipfile.ZIP_LZMA
}

def make_zip_builtin(file_items, out_path:str, method:str, level:int):
    count=0
    input_total=0
    zip_method=METHODS[method]
    if method=='store':
        chosenlevel=None
    else:
        chosenlevel=level
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out_path, mode='w',
                         compression=zip_method,
                         compresslevel=chosenlevel) as z:
        for path, arcname in file_items:
            if path.exists() and path.is_file():
                count+=1
                input_total+=path.stat().st_size
                z.write(filename=path, arcname=arcname)
                logging.info('Aggiungo %s -> %s', path, arcname)
    
    zip_size=Path(out_path).stat().st_size

    return {
        'files':count,
        'input_bytes':input_total,
        'zip_bytes':zip_size,
        'method':method,
        'level':chosenlevel
    }            



    