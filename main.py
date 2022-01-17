import pygame
import sys
from classes import Field, Cell

# всякие константы
BACKGROUND = pygame.Color('darkslategray')
MAIN_COLOR = pygame.Color('darkseagreen2')
DEAD_COLOR = pygame.Color('darkseagreen4')
SIZE = WIDTH, HEIGHT = 620, 670
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 50, 50
BOARDERS = 30, 90
CELL_SIZE = min((WIDTH-2*BOARDERS[0])/FIELD_WIDTH, (HEIGHT-BOARDERS[1])/FIELD_HEIGHT)
FPS = 50


def terminate():
    """выход из игры"""
    pygame.quit()
    sys.exit()


def load_screen(screen):
    """на самом деле не нужен, но экран загрузки"""
    loading_end = pygame.USEREVENT + 1
    cur_pic = 0
    cur_let = 0
    pygame.time.set_timer(loading_end, 5000, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == loading_end:
                return
        screen.fill(BACKGROUND)
        line = "LOADING..."[:cur_let]

        string_rendered = FONT.render(line, True, MAIN_COLOR)
        intro_rect = string_rendered.get_rect()
        intro_rect.centerx = WIDTH // 2
        intro_rect.centery = 70
        screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        cur_pic = (cur_pic + 1) % 30
        cur_let = (cur_let + 1) % 11
        clock.tick(10)


pygame.init()
FONT = pygame.font.Font('./pix_font.ttf', 45)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

#load_screen(screen)  # экран загрузки

field = Field(FIELD_WIDTH, FIELD_HEIGHT, (DEAD_COLOR, MAIN_COLOR), CELL_SIZE, BOARDERS)

ongoing = False

running = True

while running:
    for event in pygame.event.get():
        pressed = pygame.mouse.get_pressed(3)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # при нажатии пробела ставим на паузу или продолжаем игру
            ongoing = not ongoing
        elif event.type == pygame.MOUSEBUTTONDOWN and event.but
        elif pressed[0] or pressed[2] and ongoing:
            x, y = pygame.mouse.get_pos()
            xi, yi = x - BOARDERS[0], y - BOARDERS[1]
            if xi < 0 or yi < 0:
                continue
            i = int(xi // CELL_SIZE)
            j = int(yi // CELL_SIZE)
            if i > FIELD_WIDTH or j > FIELD_HEIGHT:
                continue
            if pressed[0]:
                field.field[j][i].set_alive(1, field.colors)
            elif pressed[2]:
                field.field[j][i].set_alive(0, field.colors)

    screen.fill(BACKGROUND)

    if ongoing:
        text = "playing"
    else:
        text = "pause"

    text_rendered = FONT.render(text, True, MAIN_COLOR)
    text_rect = text_rendered.get_rect()
    text_rect.centerx = WIDTH // 4
    text_rect.centery = BOARDERS[1] // 2
    screen.blit(text_rendered, text_rect)

    clear_rendered = FONT.render("clear", True, MAIN_COLOR)
    text_rect = clear_rendered.get_rect()
    text_rect.centerx = WIDTH // 4 * 3
    text_rect.centery = BOARDERS[1] // 2
    screen.blit(clear_rendered, text_rect)

    field.step(screen, ongoing)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
