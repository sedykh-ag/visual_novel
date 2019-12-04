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
FPS = 30
WIDTH, HEIGHT = 1340, 720
WHITE = (255, 255, 255)
GREY = (161, 161, 161)
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
                 color=BLACK,
                 font_name='arial',
                 font_size=40):
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
                                        False, #antialiasing
                                        self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass

"""Main Menu class"""
class Menu:
    def __init__(self):
        self.buttons = []
        self.title = TextObject(600,
                                100,
                                lambda: "Main Menu")
        self.new_game_button = Button(600,
                                      300,
                                      100,
                                      50,
                                      "New Game")
        self.load_game_button = Button(600,
                                      400,
                                      100,
                                      50,
                                      "Load Game")
        self.exit_button = Button(600,
                                  500,
                                  100,
                                  50,
                                  "Exit to desktop")
        self.buttons.append(self.new_game_button)
        self.buttons.append(self.load_game_button)
        self.buttons.append(self.exit_button)

    def update(self):
        pass

    def handle_events(self, type, pos):
        for b in self.buttons:
            b.handle_mouse_event(type, pos)

    def draw(self, surface):
        self.title.draw(surface)
        for b in self.buttons:
            b.draw(surface)

"""State Class"""
class State:
    def __init__(self, surface):
        self.surface = surface
        self.background = None
        self.frontground = []
        self.text = ''
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

        def draw(self):
            pass

        def handle_events(self):
            pass

"""Game Class"""
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
        """Enter menu state"""
        menu = Menu()
        self.objects.append(menu)
        self.mouse_handlers.append(menu.handle_events)

        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0)) #background picture rendering

            """End sequence"""
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
        font_name = 'Arial' # REPLACE THIS !
        font_size = 10 # REPLACE THIS !
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

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.bounds.collidepoint(pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click(self)
            self.state = 'hover'

    @property
    def back_color(self):
        return dict(normal=(200, 200, 200),
                    hover=(145, 145, 145),
                    pressed=(128, 128, 128))[self.state]

"""Resource manager"""
archive = zipfile.ZipFile('resources.zip', 'r')  # создает объект архива
temp_dir = tempfile.mkdtemp()  # временная директория
archive.extract('Backgrounds/Background1.jpg', path=temp_dir)
background_dir = str.format('{}/Backgrounds/Background1.jpg', temp_dir)

"""Initialization"""
game = Game('Карась', WIDTH, HEIGHT, "resources/Backgrounds/blank.png", FPS)
game.run()
