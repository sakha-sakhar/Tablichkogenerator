import pygame
from classes.textinput import TextInput
from classes.buttons import Button
from help_func import load_font


def add_oc_mainloop():
    running = True
    
    verdict = 0
    
    pygame.display.set_caption('Параметры персонажа')

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
                    name = name_enter.value
                    running = False
                elif cancel_btn.check_mouse(mouse) or (event.type == pygame.KEYUP and event.key == 27): # Esc
                    running = False
                    verdict = -1
            elif event.type == pygame.MOUSEMOTION:
                save_btn.check_selected(mouse)
                cancel_btn.check_selected(mouse)
        screen.fill((0, 0, 0))
        
        pygame.draw.rect(screen, (255, 255, 255), pygame.rect.Rect(*inputcoords))
        name_enter.update(events)
        name_enter.draw(screen)
        
        screen.blit(save_btn.current, save_btn.coords)
        screen.blit(cancel_btn.current, cancel_btn.coords)
        
    pygame.display.set_caption('Просмотр персонажей')
    
    return verdict, name