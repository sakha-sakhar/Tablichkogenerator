import pygame
import tkinter
import tkinter.filedialog

from classes.buttons import Button, OcButton, Area
from classes.textinput import TextInput
from data.db_session import global_init
from oc_window import view_characters
from help_func import load_image, load_font, terminate, surface_from_clipboard
from handle_json import save_meme, open_meme, get_mew_meme_id, \
     import_not_hidden, import_by_id

WIDTH0 = 1280
HEIGHT0 = 920
WIDTH1 = 1080
HEIGHT1 = 840


def create_mem_window():
    running = True
    bg = load_image('bg.png')
    bgw = bg.get_width()
    bgh = bg.get_height()
    newpic = False
    
    screen = pygame.display.set_mode((WIDTH0, HEIGHT0), pygame.RESIZABLE)
    pygame.display.set_caption('Создать мем')
    
    ocs = list(import_not_hidden())
    oc_btns = []
    for oc in ocs:
        oc_btns.append(OcButton(oc['img'], oc['id']))
    areas = []
    for i in range(6):
        areas.append(Area((215, 60 + 105 * i, 735, 160 + 105 * i)))
    '''areas.append(Area((400, 150, 600, 200)))
    areas.append(Area((400, 200, 600, 300)))
    areas.append(Area((400, 300, 600, 500)))
    areas.append(Area((400, 500, 600, 800)))'''

    texts = [TextInput(10, 60 + i * 105, 200, 100) for i in range(6)]
    title = TextInput(10, 20, 725, 40, (255, 255, 255))
    
    area_selection = False
    start_point = []
    
    m_id = get_mew_meme_id()
    
    while running:
        pygame.display.flip()
        events = pygame.event.get()
        
        oc_number_in_a_row = 0
        import_btn.coords = (screen.get_width() - 200, import_btn.coords[1])
        save_btn.coords = (screen.get_width() - 200, screen.get_height() - 50)
        open_btn.coords = (screen.get_width() - 400, screen.get_height() - 50)
        paste_btn.coords = (screen.get_width() - 400, paste_btn.coords[1])
        back_btn.coords = (screen.get_width() - 600, back_btn.coords[1])
        
        for event in events:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in oc_btns:
                    if btn.check_mouse(mouse):
                        btn.grabbed = True
                        btn.d_x = mouse[0] - btn.coords[0]
                        btn.d_y = mouse[1] - btn.coords[1]
                        break
                else:
                    if newpic: 
                        area_selection = True
                        start_point = mouse
            elif event.type == pygame.MOUSEBUTTONUP:
                for btn in oc_btns:
                    if btn.grabbed:
                        if btn.move(oc_btns, areas):
                            break
                        
                if save_btn.check_mouse(mouse):
                    areas_info = []
                    if newpic:
                        for area in areas:
                            areas_info.append({
                                'coords': area.coords,
                                'chars': [oc.id for oc in area.positions]})
                    else:
                        for area in areas:
                            areas_info.append({
                                'coords': [area.coords[0] + 10, area.coords[1] + 60,
                                           area.coords[2] + 10, area.coords[3] + 60],
                                'chars': [oc.id for oc in area.positions]})
                            
                    save_meme(areas_info, m_id)
                    if not newpic:
                        mem = pygame.surface.Surface((bgw + 10, bgh + 60))
                        mem.blit(bg, (10, 60))
                        pygame.image.save(mem, f'images/templates/{m_id}.png')
                        mem.blit(title.surface, (10, 10, 725, 40))
                        for btn in oc_btns:
                            mem.blit(btn.current, btn.coords)
                        for t in texts:
                            t.draw(mem)
                    else:
                        mem = pygame.surface.Surface((bgw, bgh))
                        mem.blit(bg, (0, 0))
                        pygame.image.save(mem, f'images/templates/{m_id}.png')
                        for btn in oc_btns:
                            mem.blit(btn.current, (btn.coords[0] - 10, btn.coords[1] - 60))
                    pygame.display.flip()
                    pygame.image.save(mem, f'result/{m_id}.png')
                    
                if import_btn.check_mouse(mouse):
                    top = tkinter.Tk()
                    top.withdraw()  # hide window
                    file_name = tkinter.filedialog.askopenfilename(parent=top)
                    top.destroy()
                    if file_name:
                        newpic = True
                        bg = load_image(file_name)
                        if bg.get_height() > 880:
                            bg = pygame.transform.rotozoom(bg, 0, 880 / bg.get_height())
                        bgw = bg.get_width()
                        bgh = bg.get_height()
                        areas = []
                        
                if back_btn.check_mouse(mouse):
                    running = False
                    
                if open_btn.check_mouse(mouse):
                    print('open pressed')
                    areas, ocs, oc_btns, m_id = open_mainloop(ocs)
                    file_name = f'templates/{m_id}.png'
                    if file_name:
                        newpic = True
                        bg = load_image(file_name)
                        bgw = bg.get_width()
                        bgh = bg.get_height()
                    
                if paste_btn.check_mouse(mouse):
                    pic = surface_from_clipboard()
                    if pic:
                        newpic = True
                        bg = pic
                        if bg.get_height() > 880:
                            bg = pygame.transform.rotozoom(bg, 0, 880 / bg.get_height())
                        bgw = bg.get_width()
                        bgh = bg.get_height()
                        areas = []
                if area_selection:
                    x1 = min(mouse[0], start_point[0])
                    y1 = min(mouse[1], start_point[1])
                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        x2 = max(mouse[0], start_point[0]) # для более гибкого выделения
                    else:
                        x2 = bgw + 10  # стандартные случаи
                    y2 = max(mouse[1], start_point[1])
                    if not (x1 == x2 or y1 == y2):
                        areas.append(Area((x1, y1, x2, y2)))
                    start_point = []
                    area_selection = False 
            elif event.type == pygame.MOUSEMOTION:
                for btn in oc_btns:
                    if btn.grabbed:
                        btn.coords = mouse[0] - btn.d_x, mouse[1] - btn.d_y
            elif event.type == pygame.KEYUP and event.key in (8, 127):
                if areas:
                    del areas[-1]
            for btn in (import_btn, save_btn, back_btn, paste_btn, open_btn):
                btn.check_selected(mouse)
                
        
        screen.fill((0, 0, 0))
        screen.blit(bg, (10, 60))
        if area_selection:
            x1 = min(mouse[0], start_point[0])
            y1 = min(mouse[1], start_point[1])
            x2 = max(mouse[0], start_point[0])
            y2 = max(mouse[1], start_point[1])
            pygame.draw.rect(screen, (255, 0, 0),
                             pygame.rect.Rect(x1, y1, x2 - x1, y2 - y1), 4)
        for area in areas:
            pygame.draw.rect(screen, (255, 0, 0),
                         pygame.rect.Rect(area.coords[0], area.coords[1],
                                          area.coords[2] - area.coords[0], area.coords[3] - area.coords[1]), 4)
        title.update(events)
        screen.blit(title.surface, (10, 10, 725, 40))
        for t in texts:
            if newpic:
                break
            t.update(events)
            t.draw(screen)
            
        oc_number_in_a_row = (screen.get_width() - bgw - 20) // 105
        if not oc_number_in_a_row:
            oc_number_in_a_row = 1
        i = 0
        for oc in oc_btns:
            if not oc.inside_a_meme and not oc.grabbed:
                oc.change_for_render((bg.get_width() + 20 + 105 * (i % oc_number_in_a_row),
                             60 + 105 * (i // oc_number_in_a_row)))
                i += 1
            screen.blit(oc.current, oc.coords)
        
        for btn in (save_btn, import_btn, back_btn, paste_btn, open_btn):
            screen.blit(btn.current, btn.coords)
    

def coincidences_window():
    pass


def menu_window():
    global screen
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP:
                if new_oc_btn.check_mouse(mouse):
                    view_characters()
                    screen = pygame.display.set_mode((WIDTH1, HEIGHT1))
                    pygame.display.set_caption('Табличкогенератор')
                elif new_mem_btn.check_mouse(mouse):
                    create_mem_window()
                    screen = pygame.display.set_mode((WIDTH1, HEIGHT1))
                    pygame.display.set_caption('Табличкогенератор')
                elif coincidences_btn.check_mouse(mouse):
                    coincidences_window()
                    pygame.display.set_caption('Табличкогенератор')
            elif event.type == pygame.MOUSEMOTION:
                new_mem_btn.check_selected(mouse)
                new_oc_btn.check_selected(mouse)
                coincidences_btn.check_selected(mouse)
            '''elif event.type == pygame.KEYUP:
                print(event.key)'''
            screen.blit(new_mem_btn.current, new_mem_btn.coords)
            screen.blit(new_oc_btn.current, new_oc_btn.coords)
            screen.blit(coincidences_btn.current, coincidences_btn.coords)


def open_mainloop(ocs):
    running = True
    
    ocs1 = [oc.id for oc in ocs]
    ocs2 = ocs1.copy()
    
    pygame.display.set_caption('Открыть мем')

    screen = pygame.display.set_mode((360, 240))
    open_btn = Button((150, 140), 'open')
    cancel_btn = Button((150, 190), 'cancel')
    inputcoords = (10, 10, 340, 80)
    id_enter = TextInput(*inputcoords)

    font = load_font('bahnschrift.ttf', 30)
    
    
    while running:
        pygame.display.flip()
        events = pygame.event.get()
        
        for event in events:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                if open_btn.check_mouse(mouse) or (event.type == pygame.KEYUP and event.key == 13): # Enter
                    try:
                        m_id = int(id_enter.value)
                    except ValueError:
                        continue
                    meme_info = open_meme(m_id)
                    oc_btns = []
                    areas = []
                    for ar in meme_info:
                        add_area = Area(ar['coords'])
                        for char in ar['chars']:
                            oc = import_by_id(char)
                            if oc.id in ocs1:
                                ocs1.remove(oc['id'])
                            if oc not in ocs2:
                                ocs2.append(oc['id'])
                            a_btn = OcButton(oc['img'], oc['id'])
                            add_area.add(a_btn)
                            a_btn.inside_a_meme = True
                            oc_btns.append(a_btn)
                        areas.append(add_area)
                    for oc_id in ocs1:
                        oc = import_by_id(oc_id)
                        oc_btns.append(OcButton(oc['img'], oc['id']))
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
        id_enter.update(events)
        id_enter.draw(screen)
        
        screen.blit(open_btn.current, open_btn.coords)
        screen.blit(cancel_btn.current, cancel_btn.coords)
        
    screen = pygame.display.set_mode((WIDTH0, HEIGHT0), pygame.RESIZABLE)
    pygame.display.set_caption('Создать мем')
    return areas, ocs, oc_btns, m_id


def main():
    mainrun = True
    while mainrun:
        menu_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()


if __name__ == '__main__':
    pygame.init()
    global_init("data/memogenerator.db")
    pygame.display.set_caption('Табличкогенератор')

    screen = pygame.display.set_mode((WIDTH1, HEIGHT1))

    new_oc_btn = Button((235, 212), 'new_oc')    
    new_mem_btn = Button((235, 322), 'new_mem')
    coincidences_btn = Button((235, 432), 'coincidences')
    save_btn = Button((802, HEIGHT0 - 50), 'save')
    open_btn = Button((602, HEIGHT0 - 50), 'open')
    import_btn = Button((880, 10), 'import')
    back_btn = Button((480, 10), 'back')
    paste_btn = Button((680, 10), 'paste')

    font = load_font('bahnschrift.ttf', 30)

    main()
    pygame.quit()
