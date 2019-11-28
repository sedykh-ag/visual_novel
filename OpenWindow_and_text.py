import math
import os
import sys
import tempfile
import zipfile
from collections import defaultdict

import pygame
from game_object import GameObject
from text_object import TextObject
from pygame.rect import Rect

"""Declarations"""
state = 'Menu'
FPS = 60
WIDTH, HEIGHT = 1340, 720
WHITE = (254, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

"""GameObject"""
class GameObject:
    def __init__(self, x, y, w, h, speed=(0,0)):
        self.bounds = Rect(x, y, w, h)
        self.speed = speed

    @property
    def left(self):
        return self.bounds.left

    @property
    def right(self):
        return self.bounds.right

    @property
    def top(self):
        return self.bounds.top

    @property
    def bottom(self):
        return self.bounds.bottom

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height

    @property
    def center(self):
        return self.bounds.center

    @property
    def centerx(self):
        return self.bounds.centerx

    @property
    def centery(self):
        return self.bounds.centery

    def draw(self, surface):
        pass

    def move(self, dx, dy):
        self.bounds = self.bounds.move(dx, dy)

    def update(self):
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)

"""TextObject"""
class TextObject:
    def __init__(self,
                 x,
                 y,
                 text_func,
                 color,
                 font_name,
                 font_size):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())

    def draw(self, surface, centralized=False):
        text_surface, self.bounds = \
            self.get_surface(self.text_func())
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2,
                   self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text,
                                        False,
                                        self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass

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

"""Button"""
class Button(GameObject):
    def __init__(self,
                 x,
                 y,
                 w,
                 h,
                 text,
                 on_click=lambda x: None,
                 padding=0):
        super().__init__(x, y, w, h)
        self.state = 'normal'
        self.on_click = on_click

        button_text_color = BLACK
        font_name = 'font' # REPLACE THIS !
        font_size = 0 # REPLACE THIS !
        self.text = TextObject(x + padding,
                               y + padding, lambda: text,
                               button_text_color,
                               font_name,
                               font_size)

    def draw(self, surface):
        pygame.draw.rect(surface,
                         self.back_color,
                         self.bounds)
        self.text.draw(surface)

"""Resource manager"""
archive = zipfile.ZipFile('resources.zip', 'r')  # создает объект архива
temp_dir = tempfile.mkdtemp()  # временная директория
archive.extract('Backgrounds/Background1.jpg', path=temp_dir)
background_dir = str.format('{}/Backgrounds/Background1.jpg', temp_dir)

"""Initialization"""
game = Game('Карась', WIDTH, HEIGHT, background_dir, FPS)
game.run()
