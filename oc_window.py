import pygame
import tkinter
import sys
import os

from classes.textinput import TextInput
from data.db_session import create_session, global_init
from classes.buttons import Button, OcButton, OcMenuComplexButton
from data.oc import Oc
from help_func import load_image, load_font, terminate, import_all_ocs

def render_ocs_on_screen():
    oclist = []
    i = 0
    for oc in import_all_ocs():
        oclist.append(OcMenuComplexButton(oc, (10 + 250 * (i % 4), 60 + 105 * (i // 4))))
        i += 1
    return oclist


def view_characters():
    running = True
    pygame.display.set_caption('Просмотр персонажей')
    screen = pygame.display.set_mode((1080, 840))
    
    back_btn = Button((10, 10), 'back')
    new_btn = Button((200, 10), 'new')
    
    ocbtns = render_ocs_on_screen()
    
    while running:
        pygame.display.flip()
        events = pygame.event.get()
        
        for event in events:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP:
                if new_btn.check_mouse(mouse):
                    add_oc_window()
                    screen = pygame.display.set_mode((1080, 840))
                    ocbtns = render_ocs_on_screen()
                elif back_btn.check_mouse(mouse):
                    running = False
                for btn in ocbtns:
                    if btn.check_mouse(mouse) == 3:
                        print('DELETED')
                        ocbtns = render_ocs_on_screen()
            elif event.type == pygame.MOUSEMOTION:
                new_btn.check_selected(mouse)
                back_btn.check_selected(mouse)
            if event.type == pygame.QUIT:
                terminate()
        
        screen.fill((0, 0, 0))
        for ocbutton in ocbtns:
            screen.blit(ocbutton.renderedpic, ocbutton.coords)
        screen.blit(new_btn.current, new_btn.coords)
        screen.blit(back_btn.current, back_btn.coords)
        

def add_oc_mainloop(img):
    running = True
    
    pygame.display.set_caption('Новый персонаж')

    screen = pygame.display.set_mode((360, 240))
    save_btn = Button((150, 140), 'save')
    cancel_btn = Button((150, 190), 'cancel')
    inputcoords = (10, 10, 340, 80)
    name_enter = TextInput(*inputcoords)

    font = load_font('bahnschrift.ttf', 30)
    
    
    while running:
        pygame.display.flip()
        events = pygame.event.get()
        
        for event in events:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP:
                if save_btn.check_mouse(mouse):
                    db_sess = create_session()
                    oc = Oc()
                    db_sess.add(oc)
                    db_sess.commit()

                    fname = f'{oc.id}.png'
                    pygame.image.save(img, 'images/' + fname)
                    oc.img = fname
                    oc.name = name_enter.value
                    oc.hidden = False
                    db_sess.commit()
                    running = False
                elif cancel_btn.check_mouse(mouse):
                    running = False
            elif event.type == pygame.MOUSEMOTION:
                save_btn.check_selected(mouse)
                cancel_btn.check_selected(mouse)
            if event.type == pygame.QUIT:
                terminate()
        screen.fill((0, 0, 0))
        
        pygame.draw.rect(screen, (255, 255, 255), pygame.rect.Rect(*inputcoords))
        name_enter.update(events)
        name_enter.draw(screen)
        
        screen.blit(save_btn.current, save_btn.coords)
        screen.blit(cancel_btn.current, cancel_btn.coords)
        
        pygame.display.set_caption('Просмотр персонажей')
    

def add_oc_window():
    top = tkinter.Tk()
    top.withdraw()
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    if file_name:
        img = load_image(file_name, None)
        add_oc_mainloop(img)