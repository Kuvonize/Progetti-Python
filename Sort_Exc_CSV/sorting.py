import pandas as pd

def read_table(path,delimiter=',',encoding='utf-8',sheet=None):
    if path.endswith('.csv'):
        df=pd.read_csv(path,sep=delimiter,encoding=encoding)
    elif path.endswith('.xlsx') or path.endswith('.xls'):
        if sheet is None:
            sheet_name=0
        else:
            sheet_name=sheet    
        df=pd.read_excel(path,sheet_name,engine='openpyxl')
    else:
        raise ValueError('Formato non supportato. Usa CSV o Excel')
    
    return df

def prepare_columns(df,by,style):
    nuove_colonne=[]
    for column in by:
        if style=='numeric':
            df[column] = pd.to_numeric(df[column], errors='coerce')
            nuove_colonne.append(column)

        elif style=='date':
            df[column] = pd.to_datetime(df[column], dayfirst=True, errors='coerce')
            nuove_colonne.append(column)

        elif style=='ci-string':
            df[column + "_ci"] = df[column].astype(str).str.casefold()
            nuove_colonne.append(column+'_ci')

        elif style=='string':
            nuove_colonne.append(column)

        elif style=='auto':
            col_orig=df[column].copy()
            df[column] = pd.to_numeric(df[column], errors='coerce')
            validi = df[column].notna().sum()
            totali = len(df[column])
            if validi / totali > 0.7:
                nuove_colonne.append(column)
                continue
            
            df[column] = pd.to_datetime(df[column], dayfirst=True, errors='coerce')
            validi_date=df[column].notna().sum()
            if validi_date/totali > 0.7:
                nuove_colonne.append(column)
                continue    
            else:
                df[column]=col_orig
                nuove_colonne.append(column)    
        elif style=='natural':
            nuove_colonne.append(column)

    return df, nuove_colonne    

def apply_sort(df,colonne,ascending,na_pos):
    df_sorted=df.sort_values(
        by=colonne,
        ascending=ascending,
        na_position=na_pos
    ) 
    return df_sorted

def write_table(df,output_path,delimiter,encoding,sheet='Foglio1'):
    if output_path.endswith('.csv'):
        df.to_csv(
            output_path,
            index=False,
            sep=delimiter,
            encoding=encoding,
        )
    elif output_path.endswith('.xlsx') or output_path.endswith('.xls'):
        df.to_excel(
            output_path,
            index=False,
            engine='openpyxl',
            sheet_name=sheet,
        )
    else:
        raise ValueError('Formato non supportato')    