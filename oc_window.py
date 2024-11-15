import pygame

from classes.textinput import TextInput
from classes.buttons import Button, OcMenuComplexButton, Arrow, TagButton
from help_func import load_font, terminate, oc_load_image, crop_image, surface_from_clipboard, \
     load_image, tag_standard, file_dialog
from handle_json import import_all_ocs, import_by_id, new_oc, edit_oc, get_tags, tag_filter, get_current_db
from oc_create_edit_window import add_oc_mainloop

SIZE = (1016, 610)

pygame.font.init()
font = load_font('bahnschrift.ttf', 30)


def render_ocs_on_screen(current_page, arrows, size):  # size - (столбцы, строки)
    all_ocs = import_all_ocs()
    oclist = []
    i = 0
    cols = size[0]
    rows = size[1]
    n = cols * rows
    page_max = (len(all_ocs) - 1) // n
    if current_page > page_max:
        current_page = page_max
    elif current_page < 0:
        current_page = 0
    for oc in all_ocs[current_page * n:current_page * n + n]:
        oclist.append(OcMenuComplexButton(oc, (10 + 250 * (i % cols), 60 + 105 * (i // cols)), get_current_db()))  # 4 в строчку * 7 в столбик = 28 на страницу
        i += 1
    if current_page > 0:
        arrows[0].current = arrows[0].imgs[1]
    else:
        arrows[0].current = arrows[0].imgs[0]
    
    if current_page < page_max:
        arrows[1].current = arrows[1].imgs[1]
    else:
        arrows[1].current = arrows[1].imgs[0]
    page_srf = font.render(f"{current_page + 1} / {page_max + 1}", True, (255, 255, 255))
    return oclist, arrows, current_page, page_srf


def view_characters():
    global SIZE
    taglist = ['Все', 'Актуальные'] + list(get_tags())
    current_page = 0
    running = True
    pygame.display.set_caption('Просмотр персонажей')
    screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
    
    cols = SIZE[0] // 250
    rows = (SIZE[1] - 185) // 105 
    
    back_btn = Button((10, 10), 'back')
    load_btn = Button((200, 10), 'load')
    paste_btn = Button((390, 10), 'paste')
    arrows = [Arrow('arrow', (600, 10)), Arrow('arrow', (650, 10), reverse=True)]
    
    filter_text = load_image('filter.png')
    tagbtns = []
    for tg in range(len(taglist)):
        tagbtns.append(TagButton(taglist[tg], (150 + tg // 3 * 210, SIZE[1] - 120 + tg % 3 * 35)))
    
    ocbtns, arrows, current_page, pg_sf = render_ocs_on_screen(current_page, arrows, (cols, rows))
    
    while running:
        pygame.display.flip()
        events = pygame.event.get()
        
        for event in events:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.locals.VIDEORESIZE:
                w, h = event.size
                w = max(1016, w)
                h = max(290, h)
                SIZE = (w, h)
                screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
                cols = SIZE[0] // 250
                rows = (SIZE[1] - 185) // 105
                ocbtns, arrows, current_page, pg_sf = render_ocs_on_screen(current_page, arrows, (cols, rows))
                for tg in range(len(taglist)):
                    tagbtns[tg].coords = (150 + tg // 3 * 210, SIZE[1] - 120 + tg % 3 * 35)
            elif event.type == pygame.MOUSEBUTTONUP:
                if load_btn.check_mouse(mouse):
                    v, info = add_oc_window()
                    if v == 0:
                        new_oc(crop_image(info['img']), info)
                    screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
                    ocbtns, arrows, current_page, pg_sf = render_ocs_on_screen(current_page, arrows, (cols, rows))
                elif back_btn.check_mouse(mouse):
                    running = False
                elif paste_btn.check_mouse(mouse):
                    pic = surface_from_clipboard()
                    if pic:
                        v, info = add_oc_mainloop()
                        if v == 0:
                            new_oc(crop_image(pic), info)
                        screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
                    ocbtns, arrows, current_page, pg_sf = render_ocs_on_screen(current_page, arrows, (cols, rows))
                elif arrows[0].check_mouse(mouse):  # - страница
                    current_page -= 1
                    ocbtns, arrows, current_page, pg_sf = render_ocs_on_screen(current_page, arrows, (cols, rows))
                elif arrows[1].check_mouse(mouse):  # + страница
                    current_page += 1
                    ocbtns, arrows, current_page, pg_sf = render_ocs_on_screen(current_page, arrows, (cols, rows))
                    
                for btn in ocbtns:   # проверка каждой кнопки с персонажем
                    code = btn.check_mouse(mouse)
                    if code == 4:   # edit
                        char = import_by_id(btn.related_oc['id'])
                        v, info = add_oc_mainloop(char['name'], int(char['relevant']), char['tags'])
                        if v == 0:
                            edit_oc(btn.related_oc['id'], info)
                        screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
                    if code:  # перерендерить если хоть чето нажали
                        ocbtns, arrows, current_page, pg_sf = render_ocs_on_screen(current_page, arrows, (cols, rows))
                        break
                tag_refilter = False
                tags = []
                for btn in tagbtns:  # проверка теговых кнопок
                    if btn.check_mouse(mouse):
                        btn.change_state()
                        tag_refilter = True
                    if btn.state:
                        tags.append(btn.name)
                if tag_refilter:
                    tag_filter(tag_standard(tags))
                    ocbtns, arrows, current_page, pg_sf = render_ocs_on_screen(current_page, arrows, (cols, rows))
            elif event.type == pygame.MOUSEMOTION:
                load_btn.check_selected(mouse)
                back_btn.check_selected(mouse)
                paste_btn.check_selected(mouse)
                for btn in tagbtns:
                    btn.check_selected(mouse)
            if event.type == pygame.QUIT:
                terminate()
        
        screen.fill((0, 0, 0))
        for ocbutton in ocbtns:
            screen.blit(ocbutton.renderedpic, ocbutton.coords)
        for btn in (load_btn, back_btn, paste_btn, *arrows, *tagbtns):
            screen.blit(btn.current, btn.coords)
        screen.blit(filter_text, (10, SIZE[1] - 120))
        screen.blit(pg_sf, (700, 10))
    

def add_oc_window():
    file_name = file_dialog
    if file_name:
        img = oc_load_image(file_name)
        v, inf = add_oc_mainloop()
        inf['img'] = img
        return (v, inf)
    return (-1, {})