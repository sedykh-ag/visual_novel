import math
import os
import sys
import tempfile
import zipfile

import pygame
from pygame.locals import *

"""Resource manager"""
archive = zipfile.ZipFile('resources.zip', 'r')  # создает объект архива
temp_dir = tempfile.mkdtemp()  # временная директория
archive.extract('Backgrounds/Background1.jpg', path=temp_dir)
background_dir = str.format('{}/Backgrounds/Background1.jpg', temp_dir)

pygame.init()
w, h = 1340, 720
screen = pygame.display.set_mode((w, h))  # создание окна
pygame.display.set_caption('Приключение Карася-тян')  # название окна
running = True

state = 'Menu'

WHITE = (254, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

widht_button = 200
height_button = 80

font = pygame.font.SysFont(None, 30)  # шрифт
# text = go.Text('GameFiles.zip')

# ball = pygame.image.load(text.text, namehint = "")
screen.fill(WHITE)


def menu(mouse):
    if w / 2 - 100 + widht_button > mouse.get_pos()[0] > w / 2 - 100 and h / 3 - 30 + height_button > mouse.get_pos()[
        1] > h / 3 - 30:
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


def game(c):
    c.draw()


class slide():
    def __init__(self, background_dir, text_dir, character_dir):
        temp_dir = tempfile.mkdtemp()  # временная директория
        archive.extract(background_dir, path=temp_dir)
        self.background_dir = str.format('{}/' + background_dir, temp_dir)

        temp_dir = tempfile.mkdtemp()  # временная директория
        archive.extract(text_dir, path=temp_dir)
        self.temp_dir = str.format('{}/' + text_dir, temp_dir)

        temp_dir = tempfile.mkdtemp()  # временная директория
        archive.extract(character_dir, path=temp_dir)
        self.character_dir = str.format('{}/' + character_dir, temp_dir)

    def draw(self):
        screen.blit(pygame.image.load(self.background_dir), (0, 0))
        screen.blit(pygame.image.load(self.character_dir), (0, 0))


c1 = slide('Backgrounds/Background1.jpg', 'Texts/Scene1/Text1', 'Characters/Lena/Lena_1.png')

if __name__ == "__main__":
    while running:  # Основной цикл
        for event in pygame.event.get():
            if event.type == QUIT:  # Без этого не будет работать кнопка закрыть
                running = False
        mouse = pygame.mouse
        if state == 'Menu':
            menu(mouse)
        if state == 'Game':
            game(c1)
        pygame.display.update()
pygame.quit()
