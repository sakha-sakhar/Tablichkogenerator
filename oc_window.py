import pygame
import tkinter

from classes.textinput import TextInput
from data.db_session import create_session
from classes.buttons import Button, OcMenuComplexButton, Arrow
from data.oc import Oc
from help_func import load_font, terminate, import_all_ocs, oc_load_image, crop_image, surface_from_clipboard, \
     new_oc, edit_oc
from oc_create_edit_window import add_oc_mainloop

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
                    v, name, pic = add_oc_window()
                    if v == 0:
                        new_oc(crop_image(pic), name)
                    screen = pygame.display.set_mode((1080, 840))
                    ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
                elif back_btn.check_mouse(mouse):
                    running = False
                elif paste_btn.check_mouse(mouse):
                    pic = surface_from_clipboard()
                    if pic:
                        v, name = add_oc_mainloop()
                        if v == 0:
                            new_oc(crop_image(pic), name)
                        screen = pygame.display.set_mode((1080, 840))
                    ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
                elif arrows[0].check_mouse(mouse):  # - страница
                    current_page -= 1
                    ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
                elif arrows[1].check_mouse(mouse):  # + страница
                    current_page += 1
                    ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
                for btn in ocbtns:   # проверка каждой кнопки с персонажем
                    code = btn.check_mouse(mouse)
                    if code == 4:   # edit
                        v, name = add_oc_mainloop()
                        edit_oc(btn.related_oc.id, name)
                        screen = pygame.display.set_mode((1080, 840))
                    if code:  # перерендерить если хоть чето нажали
                        ocbtns, arrows, current_page = render_ocs_on_screen(current_page, arrows)
                        break
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
    

def add_oc_window():
    top = tkinter.Tk()
    top.withdraw()
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    if file_name:
        img = oc_load_image(file_name)
        return add_oc_mainloop() + [img]