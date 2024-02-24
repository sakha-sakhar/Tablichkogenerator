import pygame
from classes.textinput import TextInput
from classes.buttons import Button, Checked_field
from help_func import load_font, terminate, load_image


def add_oc_mainloop(name="", relevant=1, tags=""):
    running = True
    
    verdict = 0
    
    pygame.display.set_caption('Параметры персонажа')

    screen = pygame.display.set_mode((360, 360))
    save_btn = Button((150, 260), 'save')
    cancel_btn = Button((150, 310), 'cancel')
    
    name_inputcoords = (10, 10, 340, 40)
    name_enter = TextInput(*name_inputcoords)
    name_enter.value = name
    
    tags_inputcoords = (10, 100, 340, 60)
    tags_enter = TextInput(*tags_inputcoords)
    tags_enter.value = tags
    checked_field_relevant = Checked_field((10, 170), 'checked_small', relevant)
    tags_sign = load_image('tags.png')
    relevant_sign = load_image('relevant.png')
    r_s_c = (checked_field_relevant.coords[0] + checked_field_relevant.size[0], checked_field_relevant.coords[1])

    font = load_font('bahnschrift.ttf', 30)
    
    info = {}
    
    while running:
        pygame.display.flip()
        events = pygame.event.get()
        
        for event in events:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                if save_btn.check_mouse(mouse) or (event.type == pygame.KEYUP and event.key == 13): # Enter
                    info['name'] = name_enter.value
                    info['relevant'] = checked_field_relevant.state
                    info['tags'] = tags_enter.value
                    running = False
                elif cancel_btn.check_mouse(mouse) or (event.type == pygame.KEYUP and event.key == 27): # Esc
                    running = False
                    verdict = -1
                for field in [checked_field_relevant]:
                    if field.check_mouse(mouse):
                        field.change_state()
            elif event.type == pygame.MOUSEMOTION:
                save_btn.check_selected(mouse)
                cancel_btn.check_selected(mouse)
        screen.fill((0, 0, 0))
        
        pygame.draw.rect(screen, (255, 255, 255), pygame.rect.Rect(*name_inputcoords))
        name_enter.update(events)
        name_enter.draw(screen)
        
        pygame.draw.rect(screen, (255, 255, 255), pygame.rect.Rect(*tags_inputcoords))
        tags_enter.update(events)
        tags_enter.draw(screen)
        
        for btn in (save_btn, cancel_btn, checked_field_relevant):
            screen.blit(btn.current, btn.coords)
        screen.blit(relevant_sign, r_s_c)
        screen.blit(tags_sign, (10, 50))
        
    pygame.display.set_caption('Просмотр персонажей')
    
    return verdict, info