import os
import sys
import tempfile
import zipfile
import pygame
from collections import defaultdict

"""Declarations"""
state = 'Menu'
FPS = 60
WIDTH, HEIGHT = 1340, 720
WHITE = (255, 255, 255)
GREY = (161, 161, 161)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)


def blit_text(surface, max_width, max_height, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = max_width, max_height
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


class Menu:
    def __init__(self, clock, background_image, surface):
        self.surface = surface
        self.clock = clock
        self.background_image = background_image
        self.over = False
        self.message = None
        self.new_game_button = ButtonMenu(500, 100, 200, 100, self.menu_over, 'New Game')
        self.load_game_button = ButtonMenu(500, 300, 200, 100, self.load_game, 'Game Load')
        self.exit_button = ButtonMenu(500, 500, 200, 100, self.exit, 'Exit')
        self.buttons = [self.new_game_button, self.load_game_button, self.exit_button]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for b in self.buttons:
                    b.handle_mouse_event(event.type, event.pos)

    def exit(self):
        pygame.quit()
        sys.exit()

    def menu_over(self):
        self.over = True

    def load_game(self):
        try:
            with open("save") as save_file:
                self.save = save_file.read()
                if int(self.save) == 0 or self.save is None:
                    print('There is no any save files')
                    self.buttons.clear()
                    self.new_game_button = ButtonMenu(500, 100, 200, 100, self.menu_over, 'New Game')
                    self.load_game_button = ButtonMenu(500, 300, 200, 100, self.load_game, 'Game Load')
                    self.exit_button = ButtonMenu(500, 500, 200, 100, self.exit, 'Exit')
                    self.buttons = [self.new_game_button, self.load_game_button, self.exit_button]
                    self.message = 'There is no any save files'
                else:
                    game.current_state = slide[int(self.save) - 1]
                    self.over = True
        except IOError:
            print("An IOError has occurred!")

    def run(self):
        while not self.over:
            self.surface.blit(self.background_image, (0, 0))
            for b in self.buttons:
                b.draw(self.surface)
            if self.message:
                blit_text(self.surface, 500, 50, self.message, (10, 10), pygame.font.SysFont('Arial', 30))
            self.handle_events()
            pygame.display.update()
            self.clock.tick(FPS)


class Flags:
    def __init__(self):
        self.a = 2


class Option:
    def __init__(self, text, flag, st1, st2):
        self.text = text
        if flag:
            self.next_state = st1
        else:
            self.next_state = st2


class State:
    def __init__(self, text, characters, background_image, options):
        self.text = text
        self.characters = characters  # dict of characters and their pos [(char1, pos1), (char2, pos2) ...]
        self.background_image = background_image
        self.options = options
        # self.flags = flags

    def handle_mouse_event(self, type, pos):
        pass


class Final_State:
    def __init__(self, text, characters, background_image):
        self.text = text
        self.characters = characters  # dict of characters and their pos [(char1, pos1), (char2, pos2) ...]
        self.background_image = background_image


class Game:
    def __init__(self, initial_state):
        self.button = None
        self.buttons = []
        self.current_state = initial_state
        self.frame_rate = FPS
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.background_menu_image = pygame.transform.scale(pygame.image.load("resources/menu/background.png"),
                                                            (WIDTH, HEIGHT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                self.current_state.handle_mouse_event(event.type, event.pos)
                for i in self.buttons:
                    i.handle_mouse_event(event.type, event.pos)
                # self.button_turn1.handle_mouse_event(event.type, event.pos)
            # self.button_turn2.handle_mouse_event(event.type, event.pos)

    def enter_main_state(self):
        pass

    def turn_state(self, i):
        self.current_state = self.current_state.options[i].next_state

    def run(self):
        menu = Menu(self.clock, self.background_menu_image, self.surface)
        menu.run()
        for i in range(len(self.current_state.options)):
            self.buttons.append(
                Button(1150, 400 - i * 100, 50, 50, self.turn_state, self.current_state.options[i].text, i))

        textbox_text = self.current_state.text
        textbox_image = pygame.image.load("textbox.png")
        textbox_font = pygame.font.SysFont('Arial', 25)
        # textbox_surface = textbox_font.render(textbox_text, False, BLACK)
        while True:
            self.surface.blit(self.current_state.background_image, (0, 0))  # background
            for img, pos in self.current_state.characters:  # characters
                self.surface.blit(img, pos)
            # there should be characters

            self.surface.blit(textbox_image, (60, 600))  # textbox
            blit_text(self.surface, 1100, 300, textbox_text, (70, 620), textbox_font)

            for i in self.buttons:
                i.draw(self.surface)

            self.handle_events()  # for buttons and exit to work
            pygame.display.update()
            self.clock.tick(self.frame_rate)


class Button():
    def __init__(self, x, y, w, h, on_click, text, k):
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.on_click = on_click
        self.i = k
        self.text = text
        self.state = 'normal'  # or pressed
        if self.text != '':
            self.font = pygame.font.SysFont('Arial', 20)

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, self.rect)
        if self.text != '':
            blit_text(surface, self.w, self.h, self.text, (self.x + self.w / 3, self.y), self.font)

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_down(self, pos):
        if self.rect.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click(self.i)
            self.state = 'normal'

    @property
    def back_color(self):
        return dict(normal=(200, 200, 200),
                    pressed=(128, 128, 128))[self.state]


class ButtonMenu():
    def __init__(self, x, y, w, h, on_click, text):
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.on_click = on_click
        self.text = text
        self.state = 'normal'  # or pressed
        if self.text != '':
            self.font = pygame.font.SysFont('Arial', 20)

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, self.rect)
        if self.text != '':
            blit_text(surface, self.w, self.h, self.text, (self.x + self.w / 3, self.y), self.font)

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_down(self, pos):
        if self.rect.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click()
            self.state = 'normal'

    @property
    def back_color(self):
        return dict(normal=(200, 200, 200),
                    pressed=(128, 128, 128))[self.state]


"""Game start testing"""
# initial_state = State(None)
"""slide5 = State(None, 'Верно', [],
               [(pygame.image.load("resources/slide_3/characters/character.png"), (0, 0))],
               pygame.transform.scale(pygame.image.load("resources/slide_3/background.jpg"), (WIDTH, HEIGHT)), 'rtr', 'ffe')

slide4 = State(None, 'Верно', [slide5, slide5],
               [(pygame.image.load("resources/slide_3/characters/character.png"), (0, 0))],
               pygame.transform.scale(pygame.image.load("resources/slide_3/background.jpg"), (WIDTH, HEIGHT)), 'rtr', 'ffe')

slide3 = State(None, 'Неверно', [slide4,slide4],
               [(pygame.image.load("resources/slide_3/characters/character.png"), (0, 0))],
               pygame.transform.scale(pygame.image.load("resources/slide_3/background.jpg"), (WIDTH, HEIGHT)), 'rtr', 'ffe')

slide2 = State(slide3, 'Тебя зовут Да?', [slide3,slide4],
               [(pygame.image.load("resources/slide_2/characters/character.png"), (0, 0))],
               pygame.transform.scale(pygame.image.load("resources/slide_2/background.jpg"), (WIDTH, HEIGHT)), 'rtr', 'ffe')

slide1 = State(slide2, 'Как тебя зовут?', [slide2],
               [(pygame.image.load("resources/slide_3/characters/character.png"), (0, 0))],
               pygame.transform.scale(pygame.image.load("resources/slide_1/background.jpg"), (WIDTH, HEIGHT)), 'rtr', 'ffe')
slide = []
slide.append(slide1)
slide.append(slide2)
slide.append(slide3)
slide.append(slide5)
slide.append(slide5)"""

options3 = []
slide4 = State('3', [(pygame.image.load("resources/slide_2/characters/character.png"), (0, 0))],
               pygame.transform.scale(pygame.image.load("resources/slide_1/background.jpg"), (WIDTH, HEIGHT)), options3)
slide3 = State('3', [(pygame.image.load("resources/slide_3/characters/character.png"), (0, 0))],
               pygame.transform.scale(pygame.image.load("resources/slide_3/background.jpg"), (WIDTH, HEIGHT)), options3)
option21 = Option('да', 1, slide3, slide4)
option22 = Option('нет', 1, slide4, slide3)
options2 = [option21, option22]
slide2 = State('2', [(pygame.image.load("resources/slide_2/characters/character.png"), (0, 0))],
               pygame.transform.scale(pygame.image.load("resources/slide_2/background.jpg"), (WIDTH, HEIGHT)), options2)

option11 = Option('да', 1, slide2, slide3)
option12 = Option('нет', 1, slide3, slide2)
options1 = [option11, option12]
slide1 = State('1', [(pygame.image.load("resources/slide_1/characters/character.png"), (0, 0))],
               pygame.transform.scale(pygame.image.load("resources/slide_1/background.jpg"), (WIDTH, HEIGHT)), options1)
slide = [slide1, slide2, slide3]

game = Game(slide[0])
game.run()
