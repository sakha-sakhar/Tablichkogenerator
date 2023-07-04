import os
import sys
import pygame


from data.db_session import create_session, global_init
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
    
    

def import_all_ocs():
    db_sess = create_session()
    return db_sess.query(Oc).all()


def import_not_hidden():
    db_sess = create_session()
    return db_sess.query(Oc).filter_by(hidden=False)


def oc_change_hidden_state(oc_id):
    db_sess = create_session()
    db_sess.query(Oc).filter_by(id=oc_id).update({'hidden': not db_sess.query(Oc).filter_by(id=oc_id).first().hidden})
    db_sess.commit()


def oc_delete(oc_id):
    pass