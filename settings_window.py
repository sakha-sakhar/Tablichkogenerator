import pygame

from classes.textinput import TextInput
from classes.buttons import Button, OcMenuComplexButton, Arrow, TagButton, db_Button
from help_func import load_font, terminate, oc_load_image, crop_image, surface_from_clipboard, \
     load_image, tag_standard
from handle_json import import_all_ocs, import_by_id, new_oc, edit_oc, get_tags, tag_filter, get_current_db, get_db_ids, \
     change_current_db, new_db, rename_db, del_db
from oc_create_edit_window import add_oc_mainloop
from handle_zip import save_db, import_db

pygame.font.init()
font = load_font('bahnschrift.ttf', 30)

def rerender_db_btns():
    return [db_Button(db_id[1], (10, 100 + 55 * db_id[0]), active=int(get_current_db() == db_id[1])) for db_id in enumerate(get_db_ids())]

def settings_window(screen):
    running = True
    pygame.display.set_caption('Настройки')
    
    back_btn = Button((10, 10), 'back')
    dbtext = font.render("База данных", True, (255, 255, 255))
    plus_btn = Button((210, 50), 'plus')
    save_db_btn = Button((210, 0), 'save_db')
    load_db_btn = Button((260, 0), 'load_db')
    db_btns = rerender_db_btns()

    while running:
        pygame.display.flip()
        events = pygame.event.get()
        
        for event in events:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP:
                if back_btn.check_mouse(mouse):
                    running = False
                elif plus_btn.check_mouse(mouse):
                    v, name = db_name(screen)
                    if not v:
                        new_db(name)
                    pygame.display.set_caption('Настройки')
                    db_btns = rerender_db_btns()
                elif save_db_btn.check_mouse(mouse):
                    save_db(get_current_db())
                elif load_db_btn.check_mouse(mouse):
                    import_db()
                    db_btns = rerender_db_btns()
                for btn in db_btns:
                    code = btn.check_mouse(mouse)
                    if code == 1:
                        change_current_db(btn.id)
                    elif code == 2:
                        v, name = db_name(screen, start=btn.name)
                        if not v:
                            rename_db(btn.id, name)
                        pygame.display.set_caption('Настройки')
                    elif code == 3:
                        del_db(btn.id)
                    if code:
                        db_btns = rerender_db_btns()
            elif event.type == pygame.MOUSEMOTION:
                for btn in (back_btn, plus_btn, save_db_btn, load_db_btn, *db_btns):
                    btn.check_selected(mouse)
        
        screen.fill((0, 0, 0))
        screen.blit(dbtext, (20, 60))
        for btn in (back_btn, plus_btn, save_db_btn, load_db_btn, *db_btns):
            screen.blit(btn.current, btn.coords)
            
            
def db_name(screen, start=''):
    running = True
    
    pygame.display.set_caption('Введите название')

    save_btn = Button((10, 100), 'save')
    cancel_btn = Button((190, 100), 'cancel')
    inputcoords = (10, 10, 350, 80)
    
    name_enter = TextInput(*inputcoords)
    name_enter.value = start
    v = 0
    name = ""
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
                    name = name_enter.value
                    running = False
                elif cancel_btn.check_mouse(mouse) or (event.type == pygame.KEYUP and event.key == 27): # Esc
                    running = False
                    v = -1
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
        
    return v, name