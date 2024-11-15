import pygame
from handle_json import get_current_db, tag_filter, get_chars_by_tags
from get_tags_window import get_tags_window
from help_func import load_image, load_font, terminate, tag_standard, surface_antialias_resize, circle_from_square, resize_to_circle
from classes.buttons import Button
from math import pi, sin, cos

LEGEND = {'Вражда': (0, 0, 0),
          'Ненависть': (200, 36, 36),
          'Знакомые': (200, 200, 100),
          'Друзья': (40, 140, 40),
          'Лучшие друзья': (0, 210, 150),
          'Семья': (0, 80, 120),
          'Влюбл-ть': (255, 50, 170),
          'Любовь': (140, 0, 80),
          'ОТП': (250, 128, 250),
          'БроОТП': (110, 150, 220),
          'НоОТП': (200, 140, 30),}

def circles_window():
    CURRENT_DB = get_current_db()
    tags = get_tags_window(CURRENT_DB)

    ######
    
    chars = get_chars_by_tags(tag_standard(tags))
    print(chars)
    
    height = 2000
    delta = 60
    alpha = 0.2
    margin = 0.33
    font = load_font('bahnschrift.ttf', height//25)
    img = pygame.surface.Surface((height, height))
    n = len(chars)
    img.fill((255, 255, 255))
    main_circle_centre = (height // 2 * (1 + alpha), height//2)
    main_circle_radius = height // 2 * (1 - alpha) * 0.8
    # pygame.draw.circle(img, (255, 0, 0), main_circle_centre, main_circle_radius)
    size = round(pi * main_circle_radius * 2 // (n  * (1 + margin)))
    if size > height // 5:
        size = height // 5
    
    gamma = 2 * pi / n
    for i in range(n):
        pic = load_image(f'db_{CURRENT_DB}/{chars[i]["img"]}')
        pic = resize_to_circle(pic, (size, size))
        img.blit(pic, (round(main_circle_centre[0] + sin(gamma * i) * main_circle_radius - size / 2),
                       round(main_circle_centre[1] + cos(gamma * i) * main_circle_radius - size / 2)))
        # pygame.draw.circle(img, (0, 0, 0), (round(main_circle_centre[0] + sin(gamma * i) * main_circle_radius),
        #                                    round(main_circle_centre[1] + cos(gamma * i) * main_circle_radius)), size // 2)
    iterator = 0 
    for pos in LEGEND:
        pygame.draw.circle(img, LEGEND[pos], (height // 30, height // 20 * (1 + iterator)), height//50)

        img.blit(font.render(pos, True, LEGEND[pos]), (height // 15, height // 20 * (0.6 + iterator)))
        iterator += 1
    pygame.image.save(img, f'result/{CURRENT_DB}/circles.png')
    
    windowsize = 900
    screen = pygame.display.set_mode((windowsize, windowsize + delta))
    pygame.display.set_caption('Кружочки')

    running = True
    
    back_btn = Button((10, 10), 'back')
    screen.blit(img, (0, delta))
    
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
            for btn in [back_btn]:
                btn.check_selected(mouse)
        
        for btn in [back_btn]:
            screen.blit(btn.current, btn.coords)