import json

def open_db(name):
    return json.load(open(name, 'r'))


def get_mew_meme_id():
    db = open_db('memes_db.json')
    a = 0
    for i in db.keys():
        if int(i) > a:
            a = int(i)
    return str(a + 1)


def save_meme(areas_info, m_id):
    db = open_db('memes_db.json')
    db[m_id] = areas_info
    with open('memes_db.json', 'w') as f:
        f.write(json.dumps(db))
    

def open_meme(m_id):
    db = open_db('memes_db.json')
    return db[str(m_id)]
        
        
    
