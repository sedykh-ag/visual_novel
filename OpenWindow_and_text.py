import pygame
import math, sys, os
from pygame.locals import *

pygame.init()
w, h = 640, 240
screen = pygame.display.set_mode((w, h))  #создание окна
pygame.display.set_caption('Приключение Карасика')  #название окна
running = True
BLUE = (0, 0, 255)
font = pygame.font.SysFont(None, 24)       # шрифт
img = font.render('hellowqqek', True, BLUE)  # его рендер
screen.blit(img, (20, 20))                 # вывод на экран
while running: # Основной цикл
    for event in pygame.event.get():
        if event.type == QUIT: # Без этого не будет работать кнопка закрыть
            running = False
    pygame.display.update()
pygame.quit()
