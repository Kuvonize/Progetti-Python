import zipfile
import json
from pathlib import Path
from .huffman import compress_bytes
from datetime import datetime
import logging

def make_zip_huffman(file_items, out_path:str):
    manifest=[]
    files=0
    input_total=0
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, 'w', compression=zipfile.ZIP_STORED) as z:
        for (path,arcname) in file_items:
            try:
                data=path.read_bytes()
            except OSError:
                logging.warning(f'{path} non esiste')
                continue
            blob, info= compress_bytes(data)
            z.writestr(arcname+'.huf', blob)
            files+=1
            input_total+=info['original_size']
            manifest.append({
                'original_path': str(path),
                'stored_as': arcname + ".huf",
                'original_size': info["original_size"],
                'compressed_size': info["compressed_size"],
                'bit_length': info["bit_length"]  
            })
        manifest_obj={
            "files": manifest,
            "archive_created": datetime.now().isoformat(timespec="seconds"),
            "algorithm": "huffman"
        }
        z.writestr('MANIFEST.json', json.dumps(manifest_obj, ensure_ascii=False, indent=2))
    zip_bytes=Path(out_path).stat().st_size
    return {
        'files':files,
        'input_bytes':input_total,
        'zip_bytes':zip_bytes,
        'method':'huffman'
    }        