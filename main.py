import pygame
import pygame_gui
import sys
import os

FPS = 50

pygame.init()
size = WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data\\theme.json')


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def show_statistic():
    pass

def start_screen():

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((342, 300), (150, 75)),
                                                text='Начать игру',
                                                manager=manager)
    statistic_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((342, 400), (150, 75)),
                                                text='Статистика',
                                                manager=manager)

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    return
                if event.ui_element == statistic_button:
                    show_statistic()
            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                pygame.draw.rect(screen, (91, 35, 0), (x + 2, y + 2, self.cell_size - 4, self.cell_size - 4))


def draw(screen, score):
    screen.fill((0, 0, 0))
    screen.blit(border_image, (0, 60))
    screen.blit(wood, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(str(score), True, (156, 20, 20))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = 30 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))

start_screen()
screen.fill((0, 0, 0))
border_image = pygame.transform.scale(load_image('field_fon.png'), (WIDTH, WIDTH + 5))
wood = load_image('wood.png')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    draw(screen, 0)
    pygame.display.flip()
    clock.tick(FPS)