import json
from help_func import img_save, new_folders_for_db, import_from_folder

DB_DB = 'data/db_db.json'

def open_db(name):
    return json.load(open(name, 'r'))

def save_db(name, db):
    with open(name, 'w') as f:
        f.write(json.dumps(db))

def get_current_db():
    return open_db(DB_DB)['current']

def get_memes_db():
    return f'data/{get_current_db()}_memes_db.json'

def get_chars_db():
    return f'data/{get_current_db()}_chars_db.json'


# DB DB

def get_db_ids():
    ids = list(open_db(DB_DB).keys())
    ids.remove('current')
    return ids

def get_db_name(id):
    return open_db(DB_DB)[str(id)]

def change_current_db(id):
    data = open_db(DB_DB)
    data['current'] = str(id)
    save_db(DB_DB, data)

def get_new_db_id():
    db = open_db(DB_DB)
    values = list(db.keys())
    values.remove('current')
    try:
        a = max(list(map(lambda i: int(i), values)))
    except ValueError:
        a = 0
    return a + 1

def new_db(name, source=""):
    db = open_db(DB_DB)
    new_id = str(get_new_db_id())
    db[new_id] = name
    db['current'] = new_id
    save_db(DB_DB, db)
    if source:
        import_from_folder(source, new_id)
        return new_id
    new_folders_for_db(new_id)
    ch_db = open(f"data/{new_id}_chars_db.json", "w+")
    ch_db.write(json.dumps({}))
    mem_db = open(f"data/{new_id}_memes_db.json", "w+")
    mem_db.write(json.dumps({}))
    ch_db.close()
    mem_db.close()
    return new_id
    
def rename_db(id, name):
    db = open_db(DB_DB)
    db[id] = name
    save_db(DB_DB, db)
    

def del_db(id):
    db = open_db(DB_DB)
    del db[id]
    save_db(DB_DB, db)
    
# МЕМИ

def get_mew_meme_id():
    MEMES_DB = get_memes_db()
    db = open_db(MEMES_DB)
    try:
        a = max(list(map(lambda i: int(i), db.keys())))
    except ValueError:
        a = 0
    return a + 1

def save_meme(areas_info, m_id):
    MEMES_DB = get_memes_db()
    db = open_db(MEMES_DB)
    db[m_id] = areas_info
    save_db(MEMES_DB, db)
    

def open_meme(m_id):
    MEMES_DB = get_memes_db()
    db = open_db(MEMES_DB)
    return db[str(m_id)]


##### ПЕРСЫ

# Импорты
    
def import_all_ocs():  # сразу происходит сортировка в порядке видимые > актуальные > остальные
    CHARS_DB = get_chars_db()
    db = open_db(CHARS_DB)
    l1 = []
    l2 = []
    l3 = []
    for char in db:
        db[char]['id'] = char
        if db[char]['hidden'] == False:
            l1.append(db[char])
        elif db[char]['relevant'] == True:
            l2.append(db[char])
        else:
            l3.append(db[char])
    return l1 + l2 + l3     

def import_not_hidden():
    CHARS_DB = get_chars_db()
    db = open_db(CHARS_DB)
    l1 = []
    for char in db:
        db[char]['id'] = char
        if db[char]['hidden'] == False:
            l1.append(db[char])
    return l1
    
def import_by_id(n):
    CHARS_DB = get_chars_db()
    db = open_db(CHARS_DB)
    ch = db[str(n)]
    ch['id'] = n
    return ch

# Операции

def new_oc(img, info):
    CHARS_DB = get_chars_db()
    db = open_db(CHARS_DB)
    try:
        oc_id = max([int(i) for i in db.keys()]) + 1
    except ValueError:
        oc_id = 1
    fname = f'chars/{oc_id}.png'
    img_save(img, 'images/db_' + get_current_db() + '/' + fname)
    db[oc_id] = {'name': info['name'],
                 'img': fname,
                 'relevant': info['relevant'],
                 'hidden': False,
                 'tags': info['tags']}
    save_db(CHARS_DB, db)
    
def edit_oc(oc_id, info):
    CHARS_DB = get_chars_db()
    db = open_db(CHARS_DB)
    for i in info:
        db[oc_id][i] = info[i]
    save_db(CHARS_DB, db)

def oc_change_hidden_state(oc_id, state=-1, db={}):  # -1 - сменить состояние на противоположное нынешнему, state=0 или 1 - на конкретное
    CHARS_DB = get_chars_db()
    no_db = not bool(db)
    if no_db:
        db = open_db(CHARS_DB)
    if state == -1:
        db[oc_id]['hidden'] = not db[oc_id]['hidden']
    else:
        db[oc_id]['hidden'] = bool(state)
    if no_db:
        save_db(CHARS_DB, db)
    return db

def oc_delete(oc_id):
    CHARS_DB = get_chars_db()
    db = open_db(CHARS_DB)
    del db[oc_id]
    save_db(CHARS_DB, db)
    
# Теги

def get_tags():
    CHARS_DB = get_chars_db()
    db = open_db(CHARS_DB)
    tags = set()
    for i in db:
        for j in db[i]['tags']:
            if j:
                tags.add(j)
    return tags

def tag_filter(tags):
    CHARS_DB = get_chars_db()
    db = open_db(CHARS_DB) # В целях оптимизации база данных открывается один раз перед циклом 
    for char in db:
        #if ((tags in db[char]['tags'] or tags == 'Актуальные') and db[char]['relevant']) or tags == 'Все':
        if satisfies_tags(db[char], tags):
            db = oc_change_hidden_state(char, 0, db)  # и передается в обновленном виде в каждой итерации
        else:
            db = oc_change_hidden_state(char, 1, db)
    save_db(CHARS_DB, db)

def get_chars_by_tags(tags):
    CHARS_DB = get_chars_db()
    db = open_db(CHARS_DB) # В целях оптимизации база данных открывается один раз перед циклом
    charslist = []
    for char in db:
        if satisfies_tags(db[char], tags):
            charslist.append(db[char])
    return charslist
    
def satisfies_tags(char, tags):
    return ((tags[0] and char['relevant']) or not tags[0]) and all(i in char['tags'] for i in tags[1])