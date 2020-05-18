from translate.storage.tmx  import tmxfile
from polib import POFile, POEntry
from argparse import ArgumentParser


def run():
    parser = ArgumentParser()
    parser.add_argument("action",type=str,help="Action to do")
    parser.add_argument("input",type=str,help="Input file to slit to po")
    parser.add_argument("orig_lang",type=str,help="Original code language")
    parser.add_argument("dest_lang",type=str,help="Translated code language")
    parser.add_argument("--output",default="output", help="File output")
    parser.add_argument("--entries",default=20, type=int, help="Number of entries")
    args = parser.parse_args()
    
    if args.action == 'split':
        split(args.input, args.orig_lang, args.dest_lang, args.output, args.entries)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def generate_po_from_tmx(f_path, entries):
    pofile = POFile()
    for tmx_entry in entries:
        po_entry = POEntry(msgid=tmx_entry.getsource(), msgstr=tmx_entry.gettarget())
        pofile.append(po_entry)
    pofile.save(f_path)

def split( f_input, orig_lang, dest_lang, f_output, num_entries ):
    with open(f_input, 'rb') as fd:
        tmx_file = tmxfile(fd, orig_lang, dest_lang)
    postfix = "" if len(tmx_file.units) < num_entries else "1"
    for entries in chunks(tmx_file.units, num_entries):
        print(len(entries))
        generate_po_from_tmx(f_output + postfix + ".po", entries)
        postfix = str(int("0" + postfix) + 1)
        


if __name__ == "__main__":
    run()