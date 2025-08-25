import argparse
from compressors.builtin_zip import make_zip_builtin
from collectors import collect_files
from compressors.huffman_zip import make_zip_huffman


parser=argparse.ArgumentParser(prog='zip-maker', description='Crea archivi ZIP da file/cartelle')

parser.add_argument('paths', nargs='+', help='File o cartelle da includere nello zip')
parser.add_argument('-o', '--out', required=True, help='Nome del file zip di output')
parser.add_argument('--recursive', action='store_true', help='Se attivato esplora le cartelle in modo ricorsivo')
parser.add_argument('--base', type=str, help='Cartella base per i percorsi interni')
parser.add_argument('--exclude', action='append', default=[], help='Pattern di file da escludere (può essere ripetuto)')
parser.add_argument('--algo', choices=['builtin','huffman'], default='builtin',
                    help='Tipo di compressione: builtin (zip nativo) o huffman (didattico)')
parser.add_argument('--method', choices=['store','deflate','bzip2','lzma'], default='deflate',
                    help='Metodo di compressione builtin da usare nello zip')
parser.add_argument('--level', type=int, default=6, help='Livello di compressione (0–9, dipende dal metodo scelto)')

args=parser.parse_args()

def fmt(n):
        return f'{n/1024:.1f} KiB'

items = collect_files(args.paths, args.recursive, args.exclude, args.base)
if args.algo=='builtin':
    report=make_zip_builtin(items,args.out,args.method,args.level)

    print(f'File: {report["files"]}  |  Input: {fmt(report["input_bytes"])}  |  Zip: {fmt(report["zip_bytes"])}  |  {report["method"]} (lvl {report["level"]})')

if args.algo=='huffman':
    report=make_zip_huffman(items, args.out)

    print(f'File: {report["files"]}  |  Input: {fmt(report["input_bytes"])}  |  Zip: {fmt(report["zip_bytes"])}  |  {report["method"]})')