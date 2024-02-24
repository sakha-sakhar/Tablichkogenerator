import pygame

from data.oc import Oc
from data.row import Row
from data.db_session import create_session
from classes.buttons import OcCoincidencesButton, Button
from help_func import terminate, import_all_ocs, load_font

FONT = load_font(font_size=40, name='bahnschrift.ttf')


def find_coincidences(fnames):
    db_sess = create_session()
    ocs = [db_sess.query(Oc).filter_by(img=fname).first() for fname in fnames]
    rows = db_sess.query(Row).all()

    n = 0
    for row in rows:
        n += 1
        for oc in ocs:
            if row not in oc.rows:
                n -= 1
                break
    return n


def coincidences_window(screen):
    oc_btns = []

    i = 0
    for oc in import_all_ocs():
        oc_btns.append(OcCoincidencesButton(15 + 105 * (i % 10), 60 + 160 * (i // 10), oc))
        i += 1
    back_btn = Button((10, 10), 'back')

    running = True
    while running:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP:
                for btn in oc_btns:
                    btn.check_selected(mouse)
                if back_btn.check_mouse(mouse):
                    running = False
            elif event.type == pygame.MOUSEMOTION:
                back_btn.check_selected(mouse)

        to_find = []
        for btn in oc_btns:
            if btn.active:
                to_find.append(btn.oc.img)
        if len(to_find) > 1:
            text = FONT.render(str(find_coincidences(to_find)), True, (255, 255, 255))
        else:
            text = FONT.render('0', True, (255, 255, 255))
        screen.blit(text, (200, 6))
        screen.blit(back_btn.current, back_btn.coords)
        for btn in oc_btns:
            btn.draw(screen)
        pygame.display.flip()
        screen.fill((0, 0, 0))
