import pygame
import sys
import os

from help_func import load_image, load_font, oc_change_hidden_state, \
     oc_delete, oc_load_image, surface_from_clipboard, crop_image, \
     surface_antialias_resize, surface_normal_resize, tag_filter

pygame.font.init()
font = load_font('bahnschrift.ttf', 30)


class Button:
    def __init__(self, coords, name):
        self.coords = coords
        self.name = name
        self.base = load_image(name + '_base.png')
        self.selected = load_image(name + '_selected.png')
        self.current = self.base
        self.size = self.base.get_size()

    def check_mouse(self, mouse):
        if self.coords[0] < mouse[0] < self.coords[0] + self.size[0] and \
                self.coords[1] < mouse[1] < self.coords[1] + self.size[1]:
            return True
        return False

    def check_selected(self, mouse):
        if self.check_mouse(mouse):
            self.current = self.selected
        else:
            self.current = self.base
    
    
class Checked_field(Button):
    def __init__(self, coords, name='checked_small', state=0):
        self.coords = coords
        self.name = name
        self.state = state
        self.imgs = [load_image(f'{name}_0.png'), load_image(f'{name}_1.png')]
        self.current = self.imgs[state]
        self.size = self.current.get_size()
        
    def check_selected(self, mouse):
        pass
    
    def change_state(self):
        self.state = (self.state + 1) % 2
        self.current = self.imgs[self.state]


class TagButton(Button):
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords
        self.current = font.render(name, True, (255, 255, 255))
        self.size = self.current.get_size()
        
    def check_selected(self, mouse):
        pass
    
    def action(self):
        print(f'pressed {self.name} filter')
        tag_filter(self.name)


class OcButton(Button):
    def __init__(self, name, oc_id):
        self.orig = load_image(name)
        self.id = oc_id
        self.current = self.orig
        self.size = self.current.get_size()
        self.coords = (0, 0)
        self.grabbed = False
        self.d_x = 0
        self.d_y = 0
        self.inside_a_meme = False

    def move(self, btns, areas):
        self.grabbed = False
        x, y = self.coords
        for area in areas:
            if self in area.positions:
                area.del_oc(self)
        for area in areas:
            if area.check_mouse((self.coords[0] + 50, self.coords[1] + 50)):
                print((area.coords[1] - 60) // 105 + 1)
                area.add(self)
                self.inside_a_meme = True
                return True
        self.inside_a_meme = False
        return False
        
    def change_for_render(self, coords, size=(100, 100)):
        self.coords = coords
        if not self.size == size:
            self.current = surface_antialias_resize(self.orig, size, self.orig.get_size())
            # self.current = surface_normal_resize(self.orig, size, self.size)
            self.size = size

            
            
class OcMenuComplexButton:
    def __init__(self, related_oc, coords):
        self.related_oc = related_oc
        self.coords = coords
        img = load_image(self.related_oc.img)
        self.img = surface_antialias_resize(img, (100, 100), img.get_size())
        self.hiddenpics = [load_image('hidden0.png'), load_image('hidden1.png')]
        self.hidden_n = int(self.related_oc.hidden)
        self.editpic = load_image('edit.png')
        self.delpic = load_image('del_small.png')
        self.name_render = font.render(self.related_oc.name, True, (255, 255, 255))
        self.renderedpic = self.render()
    
    def render(self):  # beta
        sf = pygame.surface.Surface((250, 100))
        sf.blit(self.img, (0, 0))
        sf.blit(self.hiddenpics[self.hidden_n], (100, 50))
        sf.blit(self.editpic, (150, 50))
        sf.blit(self.delpic, (200, 50))
        sf.blit(self.name_render, (105, 10))
        return sf
        
    def change_hidden_state(self):
        oc_change_hidden_state(self.related_oc.id)
        self.related_oc.hidden = not self.related_oc.hidden
        self.hidden_n = int(self.related_oc.hidden)
        self.renderedpic = self.render()

    def delete(self):
        oc_delete(self.related_oc.id)
        
    def change_pic(self):
        pic = surface_from_clipboard()
        if pic:
            self.img = crop_image(pic)
            fname = f'{self.related_oc.id}.png'
            pygame.image.save(self.img, 'images/' + fname)
            self.img = pygame.transform.scale(load_image(self.related_oc.img), (100, 100))
            self.renderedpic = self.render()

    def edit(self):  # редактирование параметров
        print(f'pressed edit ad id {self.related_oc.id}')

    def check_mouse(self, mouse):
        # print(self.related_oc.name, self.coords, mouse)
        if self.coords[0] < mouse[0] < self.coords[0] + 100 and \
                self.coords[1] < mouse[1] < self.coords[1] + 100:
            self.change_pic()
            return 1 # change_pic
        if self.coords[0] + 100 < mouse[0] < self.coords[0] + 150 and \
                self.coords[1] + 50 < mouse[1] < self.coords[1] + 100:
            self.change_hidden_state()
            return 2 # change_hidden_state
        if self.coords[0] + 150 < mouse[0] < self.coords[0] + 200 and \
                self.coords[1] + 50 < mouse[1] < self.coords[1] + 100:
            self.edit()
            return 4 # edit
        if self.coords[0] + 200 < mouse[0] < self.coords[0] + 250 and \
                self.coords[1] + 50 < mouse[1] < self.coords[1] + 100:
            self.delete()
            return 3 # delete
        return 0 
        

class Arrow(Button):
    def __init__(self, img, coords, reverse=False):
        self.imgs = pygame.transform.flip(load_image(f'{img}_0.png'), reverse, False), \
                    pygame.transform.flip(load_image(f'{img}_1.png'), reverse, False)
        self.current = self.imgs[0]
        self.coords = coords
        self.size = self.current.get_size()


class Area:
    def __init__(self, coords):  # coords - (x1, y1, x2, y2) x1 y1 - верхний левый угол обязательно
        self.coords = coords
        self.positions = []
        self.baselen = (coords[2] - coords[0]) // (coords[3] - coords[1])  # кол-во квадратиков в одной строке, если не сжимать
        self.baseheight = self.coords[3] - self.coords[1]   # высота зоны
    
    def check_mouse(self, mouse):
        if self.coords[0] < mouse[0] < self.coords[2] and \
                self.coords[1] < mouse[1] < self.coords[3]:
            return True
        return False
    
    def add(self, oc):
        if not (oc in self.positions):
            self.positions.append(oc)
        self.render()
        
    def del_oc(self, oc): # тк функция вызывается уже после проверки на наличие, ошибки быть не должно, так что тут без проверок
        self.positions.remove(oc)
        self.render()
        
    def render(self):
        height = self.baseheight  # высота одного квадратика
        width = height  # ширина одного квадратика (в пределах одной зоны они приведены к одному размеру)
        coef = 1  # сжатие ширины
        n = len(self.positions)  # кол-во квадратиков
        row = self.baselen  # количество квадратиков в строке
        nrows = 1  # количество строк
        if n > self.baselen:  # если мы не можем поместить квадратики в одну строку не сжимая
            # print(n, self.baselen, height, self.coords[2] - self.coords[0])  # ну я так дебажу, а что
            coef = width * n / (self.coords[2] - self.coords[0])  # в случае одной строки считаем во сколько раз длина несжатых квадратов превышает длину зоны
            while coef >= nrows * 2:  # nrows  - это то, во сколько раз сжимается height, следовательно если сжатие width превышает в два раза сжатие height, то картинки 
                nrows += 1            # становятся непропорциональными и надо что-то предпринять, например добавить еще одну строку
                coef = (width * n) / (self.coords[2] - self.coords[0]) / nrows   # тот же коэффициент, но мы все разделили на nrows строк, следовательно коэффициент в nrows раз меньше (я думаю проблема тут, но не факт)
            width = width // max(coef, nrows)  # собственно производим сжатие, НО если мы поделим на nrows у нас будет квадратная картинка, а если на coef - либо сжатая, либо сплющенная, сплющенная хуита так что лучше или квадрат или сжатую если сжатие необходимо, а есть coef > nrows то это так 
            row = (self.coords[2] - self.coords[0]) // width  # считаем количество квадратиков в строке чтобы потом их удобно расставить (возможно проблема тут)
            height = height // nrows  # это всегда так
            # print(n, self.baselen, height, width, coef, nrows, row)
            
        i = 0
        for oc in self.positions:
            coords = (self.coords[0] + width * (i % row), self.coords[1] + height * (i // row))
            oc.change_for_render(coords, (round(width), round(height)))
            i += 1