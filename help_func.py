import os
import sys
import pygame
from PIL import ImageGrab, Image


from data.db_session import create_session
from data.oc import Oc



def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, folder='images', colorkey=None):
    if folder:
        fullname = os.path.join(folder, name)
    else:
        fullname = name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_font(name, font_size):
    fullname = os.path.join('fonts', name)
    if not os.path.isfile(fullname):
        print(f'Файл со шрифтом {fullname} не найден')
        sys.exit()
    else:
        return pygame.font.Font(fullname, font_size)
    

def oc_load_image(name):
    original = load_image(name)
    return crop_image(original)


# Работа с базой данных    


"""def new_oc(img, name):
    db_sess = create_session()
    oc = Oc()
    db_sess.add(oc)
    db_sess.commit()

    fname = f'{oc.id}.png'
    pygame.image.save(img, 'images/' + fname)
    oc.img = fname
    oc.name = name
    oc.hidden = False
    oc.relevant = True
    db_sess.commit()
    
def edit_oc(oc_id, info):
    db_sess = create_session()
    db_sess.query(Oc).filter_by(id=oc_id).update(info)
    db_sess.commit()


def import_all_ocs():
    db_sess = create_session()
    return list(db_sess.query(Oc).filter_by(hidden=False)) + \
           list(db_sess.query(Oc).filter_by(hidden=True, relevant=True)) + \
           list(db_sess.query(Oc).filter_by(hidden=True, relevant=False))

def import_not_hidden():
    db_sess = create_session()
    return db_sess.query(Oc).filter_by(hidden=False)

def import_by_id(n):
    db_sess = create_session()
    return db_sess.query(Oc).filter_by(id=n)[0]


def oc_change_hidden_state(oc_id, state=-1):
    db_sess = create_session()
    if state == -1:
        db_sess.query(Oc).filter_by(id=oc_id).update({'hidden': not db_sess.query(Oc).filter_by(id=oc_id).first().hidden})
    else:
        db_sess.query(Oc).filter_by(id=oc_id).update({'hidden': bool(state)})
    db_sess.commit()


def oc_delete(oc_id):
    db_sess = create_session()
    db_sess.query(Oc).filter_by(id=oc_id).delete()
    db_sess.commit()

def get_tags():
    db_sess = create_session()
    chars = db_sess.query(Oc)
    tags = set()
    for i in chars:
        for j in i.tags.split(', '):
            tags.add(j)
    return tags

def tag_filter(tag):
    db_sess = create_session()
    for oc in db_sess.query(Oc):
        if tag in oc.tags and oc.relevant:
            oc_change_hidden_state(oc.id, 0)
        else:
            oc_change_hidden_state(oc.id, 1)"""

    
###  Работа с картинками    
    
def crop_image(image):
    x, y = image.get_size()
    return image.subsurface(((x - min(x, y)) // 2, (y - min(x, y)) // 2, min(x, y), min(x, y)))

def surface_from_clipboard():
    img = ImageGrab.grabclipboard()
    if not img:
        return None
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)


def surface_antialias_resize(surface, size, orig_size):
    string = pygame.image.tostring(surface, "RGBA",False)
    pic = Image.frombytes("RGBA", orig_size, string)
    pic = pic.resize(size, Image.ANTIALIAS)
    return pygame.image.fromstring(pic.tobytes(), pic.size, pic.mode)


def surface_normal_resize(surface, size, orig_size):
    return pygame.transform.scale(surface, size)