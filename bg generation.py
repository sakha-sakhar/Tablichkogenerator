import pygame

WIDTH = 1065
HEIGHT = 745


def generate_bg():
    mainrun = True
    while mainrun:
        w = 255, 255, 255
        b = 0, 0, 0

        pygame.draw.rect(screen, w, pygame.rect.Rect(10, 60, WIDTH - 340, HEIGHT - 120))

        pygame.draw.rect(screen, b, pygame.rect.Rect(110 + 100, 60, 5, HEIGHT - 120))
        pygame.draw.rect(screen, b, pygame.rect.Rect(WIDTH - 320, 60, 10, HEIGHT - 120))
        for i in range(5):
            pygame.draw.rect(screen, b, pygame.rect.Rect(10, 160 + 105 * i, WIDTH - 320, 5))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainrun = False
                pygame.image.save(screen, 'images/bg.png')
                break


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('мемогенератор какой-то')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    generate_bg()
    pygame.quit()
