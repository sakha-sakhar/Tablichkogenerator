import json

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
    print(allc)
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
    
print(cons)
        
                
    

            