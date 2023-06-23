import sys
from pathlib import Path
import os
import shutil

CATEGORIES = {'Audio': ['.mp3', '.ogg', '.wav', '.amr'],
              'Documents': ['.docx', '.txt', '.pdf', '.doc', '.xlsx', '.pptx'],
              'Images': ['.jpeg', '.png', '.jpg', '.svg'],
              'Video': ['.avi', '.mp4', '.mov', '.mkv'],
              'Archives': ['.zip', '.gz', '.tar']}

c_r = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
t_late = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

BAD_SYMBOLS = ('%', '*', ' ', '-')
TRANS = {}
for i, l in zip(c_r, t_late):
    TRANS[ord(i)] = l
    TRANS[ord(i.upper())] = l.upper()
    
for i in BAD_SYMBOLS:
    TRANS[ord(i)] = '_'

def normalize(name):
    trans_name = name.translate(TRANS)
    return trans_name

if __name__ == '__main__':
    print(normalize('****Привіт-Світ%****'))

def make_archives(path: Path):
    archive_folder = "Archives"
    for item in path.glob(f"{archive_folder}/*"):
        filename = item.stem
        arh_dir = path.joinpath(path / archive_folder / filename)
        arh_dir.mkdir()
        shutil.unpack_archive(item, arh_dir)

def del_empty_fol(path: Path):
    for fol in os.listdir(path):
        a = os.path.join(path, fol)
        if os.path.isdir(a):
            del_empty_fol(a)
            if not os.listdir(a):
                os.rmdir(a)


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        print(f'Make {target_dir}')
        target_dir.mkdir()
    if get_categories(file) == 'Other':
        file.replace(target_dir.joinpath(f'{file.stem}{file.suffix}'))
    else:
        file.replace(target_dir.joinpath(f'{normalize(file.stem)}{file.suffix}'))  

def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return 'Other'
        


def sort_folder(path: Path) -> None:

    for item in path.glob('**/*'):
        print(item)
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)            
    

def list_of_siffixes(path: Path):
    lst = set()
    lst2 = set()
    for item in path.glob('**/*'):
        if item.is_file() and item.suffix.lower() in CATEGORIES['Archives'] or item.suffix.lower() in CATEGORIES['Documents'] or item.suffix.lower() in CATEGORIES['Audio'] or item.suffix.lower() in CATEGORIES['Images'] or item.suffix.lower() in CATEGORIES['Video']:
            lst.add(item.suffix)
        elif item.is_file() and not item.suffix.lower() in CATEGORIES['Archives'] or item.suffix.lower() in CATEGORIES['Documents'] or item.suffix.lower() in CATEGORIES['Audio'] or item.suffix.lower() in CATEGORIES['Images'] or item.suffix.lower() in CATEGORIES['Video']: 
            lst2.add(item.suffix)
    print(f'Перелік усіх відомих скрипту розширень, які зустрічаються в цільовій папці:{lst}')
    print(f'Перелік всіх розширень, які скрипту невідомі:{lst2}')



def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return 'No path  to folder'
    
    if not path.exists():
        return f'Folder with path {path} doesnt exist'
    sort_folder(path)
    del_empty_fol(path)
    make_archives(path)
    list_of_siffixes(path)
    
    return 'all ok'

if __name__ == '__main__':
    print(main())