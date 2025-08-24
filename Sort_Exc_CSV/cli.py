import argparse
from sorting import read_table, prepare_columns, apply_sort, write_table
from pathlib import Path

parser = argparse.ArgumentParser(
    prog='sorter',
    description='Utility per ordinare file CSV o Excel.'
)

parser.add_argument('--input','-i', required=True, help='File di input (CSV o Excel)')
parser.add_argument('--output','-o', help='File di output ordinato')
parser.add_argument('--in-place', action='store_true', help='Sovrascrive il file di input')
parser.add_argument('--by', action='append', help='Colonna/e per ordinamento (ripetibile)')
parser.add_argument('--desc', action='append', help='Ordine discendente: true/false (ripetibile)')
parser.add_argument(
    '--style',
    choices=['auto','string','ci-string','numeric','date','natural'],
    default='auto',
    help='Stile di ordinamento'
)
parser.add_argument(
    '--na-pos',
    choices=['first','last'],
    default='last',
    help='Posizione dei valori nulli'
)
parser.add_argument("--delimiter", default=",", help="Delimitatore CSV (default ,)")
parser.add_argument("--encoding", default="utf-8", help="Encoding del file CSV (default utf-8)")
parser.add_argument("--sheet", help="Nome o indice del foglio Excel")
parser.add_argument("--dry-run", action="store_true", help="Non scrive file, mostra solo cosa farebbe")
parser.add_argument("--verbose", action="store_true", help="Mostra messaggi dettagliati")

args = parser.parse_args()

# ---- Controlli preliminari ----
p = Path(args.input)
if not p.exists():
    print("Errore: il file di input non esiste.")
    raise SystemExit(1)

if not args.by:
    print("Errore: serve almeno una colonna (--by).")
    raise SystemExit(1)

# Determina output_path
if args.in_place:
    output_path = args.input
elif args.output:
    output_path = args.output
else:
    output_path = str(p.with_name(p.stem + "_sorted" + p.suffix))

# ---- Funzione di supporto per --desc ----
def parse_bool(s: str) -> bool:
    s = s.strip().casefold()
    if s in ("true", "t", "1", "yes", "y", "on"):
        return True
    if s in ("false", "f", "0", "no", "n", "off"):
        return False
    print(f"Errore: valore non valido per --desc: {s}")
    raise SystemExit(1)

# Costruisci desc_flags e ascending
if args.desc is None:
    desc_flags = None
elif len(args.desc) == 1:
    flag = parse_bool(args.desc[0])
    desc_flags = [flag] * len(args.by)
elif len(args.desc) == len(args.by):
    desc_flags = [parse_bool(x) for x in args.desc]
else:
    print("Errore: il numero di --desc deve essere 1 oppure uguale al numero di --by.")
    raise SystemExit(1)

if desc_flags is None:
    ascending = [True] * len(args.by)
else:
    ascending = [not d for d in desc_flags]

# Safety: lunghezze coerenti
if len(ascending) != len(args.by):
    print("Errore interno: lunghezza di ascending diversa da --by.")
    raise SystemExit(1)

# ---- Pipeline ----
df = read_table(args.input, args.delimiter, args.encoding, args.sheet)
if args.verbose:
    print(f"Righe: {len(df)}  |  Colonne: {len(df.columns)}")

df, colonne_effettive = prepare_columns(df, args.by, args.style)
if args.verbose:
    print(f"Colonne effettive per l'ordinamento: {colonne_effettive}")

df_sorted = apply_sort(df, colonne_effettive, ascending, args.na_pos)

# ---- Dry-run o scrittura ----
if args.dry_run:
    print("=== DRY RUN ===")
    print(f"Input: {p}")
    print(f"Colonne (--by): {args.by}")
    print(f"Colonne effettive: {colonne_effettive}")
    print(f"Ascending: {ascending}")
    print(f"na_pos: {args.na_pos}")
    print(f"style: {args.style}")
    print(f"Output previsto: {output_path}")
else:
    write_table(df_sorted, output_path, args.delimiter, args.encoding, args.sheet)
    if args.verbose:
        print(f"Salvato in: {output_path}  |  Righe: {len(df_sorted)}  Colonne: {len(df_sorted.columns)}")



