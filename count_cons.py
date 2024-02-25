import json

def count_cons():
    db = json.load(open('data/memes_db.json', 'r'))
    
    cons = {}

    for meme in db:
        allc = set()
        con_change = {}   #  значение может быть только 1, т.е. если в одной табличке два айди пересекаются два раза
        # то это считается как 1
        for area in db[meme]:
            chars = area['chars']
            it = len(chars)
            for ch in range(it):
                allc.add(chars[ch])
                for c1 in range(ch + 1, it):
                    key = (min(int(chars[ch]), int(chars[c1])), max(int(chars[ch]), int(chars[c1])))
                    con_change[key] = con_change.get(key, [0, 0])
                    con_change[key][0] = 1
        for c in allc:
            for b in allc:
                if c != b:
                    key = (min(int(b), int(c)), max(int(b), int(c)))
                    con_change[key] = con_change.get(key, [0, 0])
                    con_change[key][1] = 1
        for i in con_change:
            cons[i] = cons.get(i, [0, 0])
            cons[i][0] += con_change[i][0]
            cons[i][1] += con_change[i][1]
    return cons


def relevant_filter_get_charslist(cons):
    db = json.load(open('data/chars_db.json', 'r'))
    chars = set()
    for pair in cons:
        if db[str(pair[0])]['relevant'] == False or \
           db[str(pair[1])]['relevant'] == False:
            del cons[pair]
        else:
            chars.add(str(pair[0]))
            chars.add(str(pair[1]))
    return cons, sorted(list(chars), key=lambda x: int(x))
