from pathlib import Path
import fnmatch
import logging


def collect_files(paths, recursive:bool, exclude_patterns: list[str], base: str|None):
    base_path=Path(base).resolve() if base else None
    lista_finale=[]
    for file in paths:
        p=Path(file)
        if not p.exists():
            logging.warning(f"{p} non esiste, salto")
            continue
        elif p.is_file():
            exclude=False
            for pattern in exclude_patterns:
                if fnmatch.fnmatch(p.name, pattern):
                    exclude=True
                    break
            if not exclude:
                if base_path:
                    try:
                        arcname=p.relative_to(base_path).as_posix()
                    except ValueError:
                        arcname=p.name
                else:
                    arcname=p.name            
                lista_finale.append((p,arcname))    
        elif p.is_dir():
            if recursive==True:
                for child in p.rglob('*'):
                    if child.is_file():
                        exclude=False
                        for pattern in exclude_patterns:
                            if fnmatch.fnmatch(child.name, pattern):
                                exclude=True
                                break
                        if not exclude:
                            if base_path:
                                try:
                                    arcname=child.relative_to(base_path).as_posix()
                                except ValueError:
                                    arcname=child.name  
                            else:
                                arcname=child.name          
                            lista_finale.append((child,arcname))    
            else:
                for child in p.glob('*'):
                    if child.is_file():
                        exclude=False
                        for pattern in exclude_patterns:
                            if fnmatch.fnmatch(child.name, pattern):
                                exclude=True
                                break
                        if not exclude:
                            if base_path:
                                try:
                                    arcname=child.relative_to(base_path).as_posix()
                                except ValueError:
                                    arcname=child.name
                            else:
                                arcname=child.name            
                            lista_finale.append((child,arcname))

    return lista_finale                                    


