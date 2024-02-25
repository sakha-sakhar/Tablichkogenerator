import os
import sys
import pygame
from PIL import ImageGrab, Image


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