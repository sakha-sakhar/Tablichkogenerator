from handle_json import get_current_db, get_tags
from help_func import terminate, load_image
from classes.buttons import TagButton, Button
import pygame


def get_tags_window(CURRENT_DB):
    
    SIZE = (500, 500)
    taglist = ['Все', 'Актуальные'] + list(get_tags())
    current_page = 0
    running = True
    pygame.display.set_caption('Фильтр')
    screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
    
    filter_text = load_image('filter.png')
    tagbtns = []
    for tg in range(len(taglist)):
        tagbtns.append(TagButton(taglist[tg], (20 + tg // 10 * 210, 70 + tg % 10 * 35)))
    
    save_btn = Button((300, 450), 'save')

    
    while running:
        pygame.display.flip()
        events = pygame.event.get()
        
        for event in events:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.locals.VIDEORESIZE:
                w, h = event.size
                w = max(500, w)
                h = max(500, h)
                SIZE = (w, h)
                screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONUP:
                for btn in tagbtns:  # проверка теговых кнопок
                    if btn.check_mouse(mouse):
                        btn.change_state()
                if save_btn.check_mouse(mouse):
                    running = False
                    tags = []
                    for btn in tagbtns:  # проверка теговых кнопок
                        if btn.state:
                            tags.append(btn.name)
            elif event.type == pygame.MOUSEMOTION:
                for btn in tagbtns:
                    btn.check_selected(mouse)
                save_btn.check_selected(mouse)
            if event.type == pygame.QUIT:
                terminate()
        
        screen.fill((0, 0, 0))
        for btn in tagbtns:
            screen.blit(btn.current, btn.coords)
        screen.blit(filter_text, (10, 10))
        screen.blit(save_btn.current, save_btn.coords)
    return tags