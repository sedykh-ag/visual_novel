import pygame
import math, sys, os
import zipfile, tempfile
from pygame.locals import *


"""Resource manager"""
archive = zipfile.ZipFile('resources.zip', 'r') # создает объект архива
temp_dir = tempfile.mkdtemp() # временная директория
archive.extract('Backgrounds/Background1.jpg', path=temp_dir)
background_dir = str.format('{}\\Backgrounds\\Background1.jpg', temp_dir)

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
    if w / 2 - 100 + widht_button > mouse.get_pos()[0] > w / 2 - 100 and 2 * h / 3 - 30 + height_button > mouse.get_pos()[1] > 2 * h / 3 - 30:
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


def game(mouse):
    print(mouse.get_pos())
    ball = pygame.image.load(background_dir)
    screen.blit(ball, (0, 0))


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
