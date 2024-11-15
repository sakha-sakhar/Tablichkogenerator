from zipfile import ZipFile
from handle_json import get_db_name, new_db
from help_func import file_dialog, get_file_name
import os

def save_db(db_id):
    with ZipFile(f'db_zip/{get_db_name(db_id)}.zip', 'w') as new_zip:
        new_zip.write(f'data/{db_id}_chars_db.json', 'chars_db.json')
        new_zip.write(f'data/{db_id}_memes_db.json', 'memes_db.json')
        for ct in ('chars', 'templates'):
            for file in os.listdir(f'images/db_{db_id}/{ct}'):
                new_zip.write(f'images/db_{db_id}/{ct}/{file}', f'{ct}/{file}')
        for file in os.listdir(f'result/{db_id}'):
            new_zip.write(f'result/{db_id}/{file}', f'res/{file}')
        
def import_db():
    file_name = file_dialog(initialdir=os.path.abspath("db_zip"), filetypes=[('ZIP базы данных', "*.zip")])
    if file_name:
        name = get_file_name(file_name)
        with ZipFile(file_name, 'r') as loaded:
            loaded.extractall('db_zip/' + name)
        new_db(name, source='db_zip/' + name)
        # os.remove(os.path.abspath('db_zip/' + name))
