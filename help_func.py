import os, os.path
import sys
import pygame
import tkinter, tkinter.filedialog
from PIL import ImageGrab, Image, ImageOps, ImageDraw
from shutil import move


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
    

def file_dialog(**kwargs):
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top, **kwargs)
    top.destroy()
    return file_name

def get_file_name(path):
    withext = os.path.split(path)[1]
    return withext.split('.')[0]

def new_folders_for_db(id):
    for i in [f'images/db_{id}', f'images/db_{id}/chars', f'images/db_{id}/templates', f'result/{id}']:
        try: 
            os.mkdir(i)
        except FileExistsError:
            pass
        
def import_from_folder(source, new_id):
    try: 
        os.mkdir(f'images/db_{new_id}')
    except FileExistsError:
        pass
    move(f'{source}/chars_db.json', f"data/{new_id}_chars_db.json")
    move(f'{source}/memes_db.json', f"data/{new_id}_memes_db.json")
    move(f"{source}/chars", f"images/db_{new_id}")
    move(f"{source}/templates", f"images/db_{new_id}")
    move(f"{source}/res", f"result/{new_id}")

def oc_load_image(name):
    original = load_image(name)
    return crop_image(original)

def percent_to_color(c1, c2, percent, c3=None):
    col = []
    if c3:
        for i in range(3):
            col.append(c1[i] * max(0, 1 - percent * 2) + c3[i] * (1 - abs(2 * percent - 1)) + c2[i] * max(0, 2 * percent - 1))
    else:
        for i in range(3):
            col.append(c2[i] * percent + c1[i] * (1 - percent))
    return tuple(col)

def img_save(img, name):
    pygame.image.save(img, name)
    
def tag_standard(tags):
    rel = 1
    if "Все" in tags:
        tags.remove('Все')
        rel = 0
    else:
        rel = 1
    if "Актуальные" in tags:
        tags.remove('Актуальные')
        rel = 1
    return [rel, tags]

###  Работа с картинками    
    
def crop_image(image):
    x, y = image.get_size()
    return image.subsurface(((x - min(x, y)) // 2, (y - min(x, y)) // 2, min(x, y), min(x, y)))

def surface_from_clipboard():
    img = ImageGrab.grabclipboard()
    if not img:
        return None
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)


def surface_antialias_resize(surface, size):
    orig_size = surface.get_size()
    string = pygame.image.tostring(surface, "RGBA",False)
    pic = Image.frombytes("RGBA", orig_size, string)
    pic = pic.resize(size, Image.LANCZOS)
    return pygame.image.fromstring(pic.tobytes(), pic.size, pic.mode)


def surface_normal_resize(surface, size):
    return pygame.transform.scale(surface, size)

def circle_from_square(surface):
    orig_size = surface.get_size()
    string = pygame.image.tostring(surface, "RGBA", False)
    pic = Image.frombytes("RGBA", orig_size, string)
    #
    mask = Image.new('L', orig_size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + orig_size, fill=255)
    output = ImageOps.fit(pic, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    #
    return pygame.image.fromstring(output.tobytes(), output.size, output.mode)

def resize_to_circle(surface, size):
    orig_size = surface.get_size()
    string = pygame.image.tostring(surface, "RGBA", False)
    pic = Image.frombytes("RGBA", orig_size, string)
    #
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(pic, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    #
    return pygame.image.fromstring(output.tobytes(), output.size, output.mode)