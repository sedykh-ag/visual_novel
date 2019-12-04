import math
import os
import sys
import tempfile
import zipfile
from random import randrange as rnd, choice
from typing import Type

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


def game(s, mouseb):
    s[0].draw()
    s[0].next(mouseb)


class Slide():
    def __init__(self, background_dir, text_dir, character_dir,
                 next_slides):  # фон,текст,герои, массив возможных следующих слайдов
        temp_dir = tempfile.mkdtemp()  # временная директория
        archive.extract(background_dir, path=temp_dir)
        self.background_dir = str.format('{}/' + background_dir, temp_dir)

        temp_dir = tempfile.mkdtemp()  # временная директория
        archive.extract(text_dir, path=temp_dir)
        self.temp_dir = str.format('{}/' + text_dir, temp_dir)

        temp_dir = tempfile.mkdtemp()  # временная директория
        archive.extract(character_dir, path=temp_dir)
        self.character_dir = str.format('{}/' + character_dir, temp_dir)

        self.next_slides = next_slides
        self.a = 0  # параметр, определяющий, куда идти дальше
        self.x = self.y = rnd(100, 200)

    def draw(self):
        screen.blit(pygame.image.load(self.background_dir), (0, 0))
        screen.blit(pygame.image.load(self.character_dir), (0, 0))

    def button(self, widht, height, mouse,x,y):  # кнопка ебать
        if w / 2 - x + widht > mouse.get_pos()[0] > w / 2 - x and h / 3 - y + height > mouse.get_pos()[
            1] > h / 3 - y:
            pygame.draw.rect(screen, (0, 50, 70), (w / 2 - x,
                                                   h / 3 - y,
                                                   widht,
                                                   height))

            if mouse.get_pressed()[0] == 1:
                self.a = 1  # пока самый простой случай - если нажат, то открывай след слайд
        else:
            pygame.draw.rect(screen, (0, 0, 0), (w / 2 - x,
                                                 h / 3 - y,
                                                 widht,
                                                 height))

    def next(self, mouse):  # функция, которая делает кнопку и рисует след. слайд. (не работает как надо)
        self.button(200, 100 , mouse, self.x, self.y)
        if self.a == 1:
            slides[self.next_slides[0]].draw()
            #slides[self.next_slides[0]].next(mouse)  # откоменчивание этой строки ведет к бесконечному циклу


slides = [0] * 10  # массив слайдов
slides[0] = Slide('Backgrounds/Background1.jpg', 'Texts/Scene1/Text1', 'Characters/Karasev/Karasev.jpg', [1])
slides[1] = Slide('Backgrounds/Background2.jpg', 'Texts/Scene1/Text1', 'Characters/Lena/Lena_2.jpg', [2])
slides[2] = Slide('Backgrounds/Background3.jpg', 'Texts/Scene1/Text1', 'Characters/Lena/Lena_2.jpg', [3])
slides[3] = Slide('Backgrounds/Background4.jpg', 'Texts/Scene1/Text1', 'Characters/Lena/Lena_2.jpg', [0])

if __name__ == "__main__":
    while running:  # Основной цикл
        for event in pygame.event.get():
            if event.type == QUIT:  # Без этого не будет работать кнопка закрыть
                running = False
        mouse = pygame.mouse
        if state == 'Menu':
            menu(mouse)
        if state == 'Game':
            game(slides, mouse)
        pygame.display.update()
pygame.quit()
