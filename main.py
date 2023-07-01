import pygame
import tkinter
import tkinter.filedialog
import sys
import os

from classes.buttons import Button, OcButton, load_image, Area
from classes.textinput import TextInput
from data.oc import Oc
from data.db_session import create_session, global_init

WIDTH = 1280
HEIGHT = 960


def load_font(name, font_size):
    fullname = os.path.join('fonts', name)
    if not os.path.isfile(fullname):
        print(f'Файл со шрифтом {fullname} не найден')
        sys.exit()
    else:
        return pygame.font.Font(fullname, font_size)


def terminate():
    pygame.quit()
    sys.exit()


def add_oc_window():
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    img = load_image(file_name, None)

    db_sess = create_session()
    oc = Oc()
    db_sess.add(oc)
    db_sess.commit()

    fname = f'{oc.id}.png'
    pygame.image.save(img, 'images/' + fname)
    oc.img = fname
    db_sess.commit()


def save():
    pass


def create_mem_window():
    bg = load_image('bg.png')
    bgw = bg.get_width()
    bgh = bg.get_height()
    newpic = False
    
    db_sess = create_session()
    ocs = db_sess.query(Oc).all()
    oc_btns = []
    for i in range(len(ocs)):
        oc_btns.append(OcButton(ocs[i].img))
    areas = []
    '''for i in range(6):
        areas.append(Area((215, 60 + 105 * i, 735, 160 + 105 * i)))'''
    areas.append(Area((400, 150, 600, 200)))
    areas.append(Area((400, 200, 600, 300)))
    areas.append(Area((400, 300, 600, 500)))
    areas.append(Area((400, 500, 600, 800)))

    texts = [TextInput(10, 60 + i * 105, 200, 100) for i in range(6)]
    title = TextInput(10, 20, 725, 40, (255, 255, 255))
    
    area_selection = False
    start_point = []

    while True:
        pygame.display.flip()
        events = pygame.event.get()
        
        oc_number_in_a_row = 0
        import_btn.coords = (screen.get_width() - 200, import_btn.coords[1])
        save_btn.coords = (screen.get_width() - 200, screen.get_height() - 50)
        
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
                    if not newpic:
                        mem = pygame.surface.Surface((bgw + 20, bgh + 40))
                        mem.blit(bg, (10, 60))
                        mem.blit(title.surface, (10, 10, 725, 40))
                        for btn in oc_btns:
                            mem.blit(btn.current, btn.coords)
                        for t in texts:
                            t.draw(mem)
                    else:
                        mem = pygame.surface.Surface((bgw, bgh))
                        mem.blit(bg, (0, 0))
                        mem.blit(title.surface, (10, 10, 725, 40))
                        for btn in oc_btns:
                            mem.blit(btn.current, (btn.coords[0] - 10, btn.coords[1] - 60))
                    pygame.display.flip()
                    pygame.image.save(mem, 'images/test.png')
                if import_btn.check_mouse(mouse):
                    newpic = True
                    top = tkinter.Tk()
                    top.withdraw()  # hide window
                    file_name = tkinter.filedialog.askopenfilename(parent=top)
                    top.destroy()
                    if file_name:
                        bg = load_image(file_name)
                        if bg.get_height() > 880:
                            bg = pygame.transform.rotozoom(bg, 0, 880 / bg.get_height())
                        bgw = bg.get_width()
                        bgh = bg.get_height()
                        areas = []
                if area_selection:
                    x1 = min(mouse[0], start_point[0])
                    y1 = min(mouse[1], start_point[1])
                    # x2 = max(mouse[0], start_point[0]) # для более гибкого выделения
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
            
        oc_number_in_a_row = (screen.get_width() - bg.get_width() - 20) // 105
        if not oc_number_in_a_row:
            oc_number_in_a_row = 1
        i = 0
        for oc in oc_btns:
            if not oc.inside_a_meme and not oc.grabbed:
                oc.change_for_render((bg.get_width() + 20 + 105 * (i % oc_number_in_a_row),
                             60 + 105 * (i // oc_number_in_a_row)))
                i += 1
            screen.blit(oc.current, oc.coords)
                
        screen.blit(save_btn.current, save_btn.coords)
        screen.blit(import_btn.current, import_btn.coords)


def coincidences_window():
    pass


def menu_window():
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP:
                if new_oc_btn.check_mouse(mouse):
                    add_oc_window()
                elif new_mem_btn.check_mouse(mouse):
                    create_mem_window()
                elif coincidences_btn.check_mouse(mouse):
                    coincidences_window()
            elif event.type == pygame.MOUSEMOTION:
                new_mem_btn.check_selected(mouse)
                new_oc_btn.check_selected(mouse)
                coincidences_btn.check_selected(mouse)
            screen.blit(new_mem_btn.current, new_mem_btn.coords)
            screen.blit(new_oc_btn.current, new_oc_btn.coords)
            screen.blit(coincidences_btn.current, coincidences_btn.coords)


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
    pygame.display.set_caption('мемогенератор какой-то')

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    new_oc_btn = Button((235, 212), 'new_oc')
    new_mem_btn = Button((235, 322), 'new_mem')
    coincidences_btn = Button((235, 432), 'coincidences')
    save_btn = Button((802, HEIGHT - 50), 'save')
    import_btn = Button((880, 10), 'import')

    font = load_font('bahnschrift.ttf', 30)

    main()
    pygame.quit()
