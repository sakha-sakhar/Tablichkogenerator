import json

MEMES_DB = 'data/memes_db.json'
CHARS_DB = 'data/chars_db.json'


def open_db(name):
    return json.load(open(name, 'r'))

def save_db(name, db):
    with open(name, 'w') as f:
        f.write(json.dumps(db))

def get_mew_meme_id():
    db = open_db(MEMES_DB)
    a = max(list(map(lambda i: int(i), db.keys())))
    return a + 1

def save_meme(areas_info, m_id):
    db = open_db(MEMES_DB)
    db[m_id] = areas_info
    save_db(MEMES_DB, db)
    

def open_meme(m_id):
    db = open_db(MEMES_DB)
    return db[str(m_id)]


##### ПЕРСЫ

# Импорты
    
def import_all_ocs():  # сразу происходит сортировка в порядке видимые > актуальные > остальные 
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
    db = open_db(CHARS_DB)
    l1 = []
    for char in db:
        db[char]['id'] = char
        if db[char]['hidden'] == False:
            l1.append(db[char])
    return l1
    
def import_by_id(n):
    db = open_db(CHARS_DB)
    ch = db[str(n)]
    ch['id'] = n
    return ch

# Операции

def new_oc(img, name, relevant):
    db = open_db(CHARS_DB)
    oc_id = max(db.keys()) + 1
    fname = f'{oc_id}.png'
    pygame.image.save(img, 'images/chars/' + fname)
    db[oc_id] = {'name': name,
                 'img': fname,
                 'relevant': relevant,
                 'hidden': False}
    save_db(CHARS_DB, db)
    
def edit_oc(oc_id, info):
    db = open_db(CHARS_DB)
    for i in info:
        db[oc_id][i] = info[i]
    save_db(CHARS_DB, db)

def oc_change_hidden_state(oc_id, state=-1, db={}):  # -1 - сменить состояние на противоположное нынешнему, state=0 или 1 - на конкретное
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
    db = open_db(CHARS_DB)
    del db[oc_id]
    save_db(CHARS_DB, db)
    
# Теги

def get_tags():
    db = open_db(CHARS_DB)
    tags = set()
    for i in db:
        for j in db[i]['tags']:
            tags.add(j)
    return tags

def tag_filter(tag):
    db = open_db(CHARS_DB) # В целях оптимизации база данных открывается один раз перед циклом 
    changes = 0
    for char in db:
        if (tag in db[char]['tags'] or tag == 'Все') and db[char]['relevant']:
            db = oc_change_hidden_state(char, 0, db)  # и передается в обновленном виде в каждой итерации
            changes += 1
        else:
            db = oc_change_hidden_state(char, 1, db)
    save_db(CHARS_DB, db)
