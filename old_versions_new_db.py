import os
from zipfile import ZipFile

with ZipFile('Старая_БД.zip', 'w') as new_zip:
    new_zip.write(f'data/chars_db.json', 'chars_db.json')
    new_zip.write(f'data/memes_db.json', 'memes_db.json')
    for ct in ('chars', 'templates'):
        for file in os.listdir(f'images/{ct}'):
            new_zip.write(f'images/{ct}/{file}', f'{ct}/{file}')
    for file in os.listdir(f'result/'):
        new_zip.write(f'result/{file}', f'res/{file}')
