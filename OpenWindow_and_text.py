import math
import os
import sys
import tempfile
import zipfile
from collections import defaultdict

import pygame
from game_object import GameObject
from text_object import TextObject
from pygame.locals import *

"""Declarations"""
state = 'Menu'
FPS = 60
WIDTH, HEIGHT = 1340, 720
WHITE = (254, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
widht_button = 200
height_button = 80

"""Resource manager"""
archive = zipfile.ZipFile('resources.zip', 'r')  # создает объект архива
temp_dir = tempfile.mkdtemp()  # временная директория
archive.extract('Backgrounds/Background1.jpg', path=temp_dir)
background_dir = str.format('{}/Backgrounds/Background1.jpg', temp_dir)

"""
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создание окна
pygame.display.set_caption('Приключение Карася-тян')  # название окна
running = True


font = pygame.font.SysFont(None, 30)  # шрифт
# text = go.Text('GameFiles.zip')

# ball = pygame.image.load(text.text, namehint = "")
screen.fill(WHITE)
"""

"""Main Game Class"""
class Game:
    def __init__(self, 
                 caption, 
                 width, 
                 height, 
                 back_image_filename, 
                 frame_rate):
        self.background_image = \
            pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def run(self):
        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
    
"""
def menu(mouse):
    if w / 2 - 100 + widht_button > mouse.get_pos()[0] > w / 2 - 100 and h / 3 - 30 + height_button > mouse.get_pos()[1] > h / 3 - 30:
        pygame.draw.rect(screen, (0, 100, 0), (w / 2 - 100,
                                               h / 3 - 30,
                                               widht_button,
                                               height_button))
        if mouse.get_pressed()[0] == 1:
            global state
            state = 'Game'

    else:
        pygame.draw.rect(screen, (0, 200, 0), (w / 2 - 100,
                                               h / 3 - 30,
                                               widht_button,
                                               height_button))
    if w / 2 - 100 + widht_button > mouse.get_pos()[0] > w / 2 - 100 and 2 * h / 3 - 30 + height_button > \
            mouse.get_pos()[1] > 2 * h / 3 - 30:
        pygame.draw.rect(screen, (0, 100, 0), (w / 2 - 100,
                                               2 * h / 3 - 30,
                                               widht_button,
                                               height_button))
    else:
        pygame.draw.rect(screen, (0, 200, 0), (w / 2 - 100,
                                               2 * h / 3 - 30,
                                               widht_button,
                                               height_button))
    new_game_text = font.render('New Game', False, BLACK)
    load_text = font.render('Load', False, BLACK)
    screen.blit(new_game_text, (w / 2 - font.size('New Game')[0] / 2, h / 3))
    screen.blit(load_text, (w / 2 - font.size('Load')[0] / 2, 2 * h / 3))

"""
"""
def game(mouse):
    print(mouse.get_pos())
    ball = pygame.image.load(background_dir)
    screen.blit(ball, (0, 0))
"""

"""
if __name__ == "__main__":
    while running:  # Основной цикл
        for event in pygame.event.get():
            if event.type == QUIT:  # Без этого не будет работать кнопка закрыть
                running = False
        mouse = pygame.mouse
        if state == 'Menu':
            menu(mouse)
        if state == 'Game':
            game(mouse)
        pygame.display.update()
pygame.quit()
"""

"""Initialization"""
game = Game('Карась', WIDTH, HEIGHT, background_dir, FPS)
game.run()
