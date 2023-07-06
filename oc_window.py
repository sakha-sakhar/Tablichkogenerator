import pygame
import tkinter

from classes.textinput import TextInput
from data.db_session import create_session
from classes.buttons import Button, OcMenuComplexButton, Arrow
from data.oc import Oc
from help_func import load_font, terminate, import_all_ocs, oc_load_image, crop_image, surface_from_clipboard

def render_ocs_on_screen(current_page, arrows):
    oclist = []
    i = 0
    all_ocs = import_all_ocs()
    page_max = (len(all_ocs) - 1) // 28
    if current_page > page_max:
        current_page = page_max
    elif current_page < 0:
        current_page = 0
    for oc in all_ocs[current_page * 28:current_page * 28 + 28]:
        oclist.append(OcMenuComplexButton(oc, (10 + 250 * (i % 4), 60 + 105 * (i // 4))))  # 4 в строчку * 7 в столбик = 28 на страницу
        i += 1
    
    if current_page > 0:
        arrows[0].current = arrows[0].imgs[1]
    else:
        arrows[0].current = arrows[0].imgs[0]
    
    if current_page < page_max:
        arrows[1].current = arrows[1].imgs[1]
    else:
        arrows[1].current = arrows[1].imgs[0]
    return oclist, arrows, current_page


def view_characters():
    current_page = 0
    running = True
    pygame.display.set_caption('Просмотр персонажей')
    screen = pygame.display.set_mode((1080, 840))
    
    back_btn = Button((10, 10), 'back')
    new_btn = Button((200, 10), 'new')
    paste_btn = Button((390, 10), 'paste')
    arrows = [Arrow('arrow', (600, 10)), Arrow('arrow', (650, 10), reverse=True)]
    
    ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
    
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
                    ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
                elif back_btn.check_mouse(mouse):
                    running = False
                elif paste_btn.check_mouse(mouse):
                    pic = surface_from_clipboard()
                    if pic:
                        add_oc_mainloop(crop_image(pic))
                        screen = pygame.display.set_mode((1080, 840))
                    ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
                elif arrows[0].check_mouse(mouse):
                    current_page -= 1
                    ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
                elif arrows[1].check_mouse(mouse):
                    current_page += 1
                    ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
                for btn in ocbtns:
                    if btn.check_mouse(mouse) == 3:
                        ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
            elif event.type == pygame.MOUSEMOTION:
                new_btn.check_selected(mouse)
                back_btn.check_selected(mouse)
                paste_btn.check_selected(mouse)
            if event.type == pygame.QUIT:
                terminate()
        
        screen.fill((0, 0, 0))
        for ocbutton in ocbtns:
            screen.blit(ocbutton.renderedpic, ocbutton.coords)
        for btn in (new_btn, back_btn, paste_btn, *arrows):
            screen.blit(btn.current, btn.coords)


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
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                if save_btn.check_mouse(mouse) or (event.type == pygame.KEYUP and event.key == 13): # Enter
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
                elif cancel_btn.check_mouse(mouse) or (event.type == pygame.KEYUP and event.key == 27): # Esc
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
        img = oc_load_image(file_name)
        add_oc_mainloop(img)