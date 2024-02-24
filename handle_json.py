import json

MEMES_DB = 'data/memes_db.json'
CHARS_DB = 'data/chars_db_test.json'


def open_db(name):
    return json.load(open(name, 'r'))

def get_mew_meme_id():
    db = open_db(MEMES_DB)
    a = 0
    for i in db.keys():
        if int(i) > a:
            a = int(i)
    return str(a + 1)


def save_meme(areas_info, m_id):
    db = open_db(MEMES_DB)
    db[m_id] = areas_info
    with open(MEMES_DB, 'w') as f:
        f.write(json.dumps(db))
    

def open_meme(m_id):
    db = open_db(MEMES_DB)
    return db[str(m_id)]


#####

    
def import_all_ocs():
    db = open_db(CHARS_DB)
    l1 = []
    l2 = []
    l3 = []
    for char in db:
        if db[char][hidden] == False:
            l1.append(db[char])
        elif db[char][relevant] == True:
            l2.append(db[char])
        else:
            l3.append(db[char])
    return l1 + l2 + l3

        
        
    
