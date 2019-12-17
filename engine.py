import os
import sys
import tempfile
import zipfile
import pygame
from tkinter import mainloop, BOTH, Canvas, Frame, Tk
from collections import defaultdict

"""Declarations"""
state = 'Menu'
FPS = 20
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


def ex(a):  # распаковка данных из архива
    temp_dir = tempfile.mkdtemp()  # временная директория
    archive.extract(a, path=temp_dir)
    a = str.format('{}/' + a, temp_dir)
    return a


class Menu:
    def __init__(self, game):
        self.surface = game.surface
        self.clock = game.clock
        self.background_image = game.background_menu_image
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
        f = open("Saves.txt", "r")
        a = f.readline()
        str = a.split()
        if a == '':
            self.message = 'There is no ane save files'
        else:
            game.current_state_index = int(str[0])
            for i in range(game.flags.n):
                game.flags.items[i] = int(str[i + 1])
                game.current_state = game.slide[game.current_state_index]
            game.run()
        f.close()

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


class Flag:
    def __init__(self, n):
        self.n = n  # кол-во элементов
        self.items = [0] * self.n


class Option:  # логическая составляющая кнопки
    def __init__(self, text, g, st1, st2, flag_use, flag_make, s):
        self.g = g  # эксземпляр класса Game, откуда импортируруется массив флагов
        self.st1 = st1  # индекс след слайда, если есть флаг
        self.st2 = st2  # индекс след слайда, если нет флага
        self.slide = s  # массив слайдов
        self.flag_use = flag_use  # флаг, который надо использовать
        self.flag_make = flag_make  # флаг, который надо поставить
        self.text = text  # текст кнопки

    def next_st(self):  # ОЧЕНЬ ВАЖНЫЙ момент, эта функция меняет массив флагов
        if self.g.flags.items[self.flag_use]:
            self.next_state = self.slide[self.st1]
            self.next_state_index = self.st1
            self.g.flags.items[self.flag_make] = 1
        else:
            self.next_state = self.slide[self.st2]
            self.next_state_index = self.st2

    def update_index(self):
        if self.g.flags.items[self.flag_use]:
            self.next_state_index = self.st1
        else:
            self.next_state_index = self.st2


class State:
    def __init__(self, text, characters, background_image, options):
        self.text = text
        self.characters = characters  # dict of characters and their pos [(char1, pos1), (char2, pos2) ...]
        self.background_image = background_image
        self.options = options  # логическая составляющая кнопок в окне

    def handle_mouse_event(self, type, pos):
        pass


def Save_Game(current_state_index, flags):  # записыват в файл индекс данного слайда и массив флагов
    a = current_state_index
    a_str = str(a)
    a_str += ' '
    f = open("Saves.txt", "w")
    f.write(a_str)
    b = [0] * flags.n
    for i in range(flags.n):
        b[i] = flags.items[i]
        b_str = str(b[i])
        b_str += ' '
        f.write(b_str)
    f.close()


class Game:
    def __init__(self, f):
        self.buttons = []
        self.frame_rate = FPS
        self.flags = f  # массив флагов
        self.first_flags = f  # начальный массив флагов
        self.a = 1  # параметр, который чутка ускоряет работу проги- показывыает, изменилось ли что-то на слайде или нет
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.buttons_surface = pygame.Surface((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.background_menu_image = pygame.transform.scale(pygame.image.load("resources/menu/background.png"),
                                                            (WIDTH, HEIGHT))

    def initialization(self, slide, i):  # костыль, необходимый для того, чтобы создать Game вначале без слайдов
        self.slide = slide
        self.current_state = slide[i]
        self.current_state_index = i

        self.first_current_state = slide[i]  # начальный слайд
        self.first_current_state_index = i  # начальный индекс

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP):
                self.current_state.handle_mouse_event(event.type, event.pos)
                for i in self.buttons:
                    i.handle_mouse_event(event.type, event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                self.a = 1

    def turn_state(self, i):  # ОЧЕНЬ ВАЖНЫЙ момент, функция, используя измененный массив флагов,
        # выдает след слайд
        self.current_state.options[i].update_index()
        self.current_state_index = self.current_state.options[i].next_state_index
        self.current_state.options[i].next_st()
        self.current_state = self.current_state.options[i].next_state

    def run_menu(self):  # запускает меню
        menu = Menu(self)
        menu.run()
        self.run()

    def run(self):
        while True:
            self.handle_events()  # for buttons and exit to work
            if self.a:
                self.buttons = []  # убирает лишние кнопки - без этого не работает
                for img, pos in self.current_state.characters:  # characters
                    self.current_state.background_image.blit(img, pos)
                    # there should be characters
                textbox_text = self.current_state.text
                textbox_image = pygame.image.load("textbox.png")
                textbox_font = pygame.font.SysFont('Arial', 25)
                self.current_state.background_image.blit(textbox_image, (60, 600))  # textbox
                blit_text(self.current_state.background_image, 1100, 300, textbox_text, (70, 620), textbox_font)

                for i in range(len(self.current_state.options)):
                    self.buttons.append(
                        Button(1150, 400 - i * 100, 50, 50, self.turn_state, self.current_state.options[i].text, i))
                self.buttons.append(
                    ButtonSave(800, 200, 80, 70, Save_Game, 'Save Game', self.current_state_index, self.flags))
                self.buttons.append(ButtonMenu(500, 500, 80, 70, self.save_and_menu, 'Go to the Menu'))
                for i in self.buttons:
                    i.draw((self.current_state.background_image))

                self.surface.blit(self.current_state.background_image, (0, 0))  # background
                pygame.display.update()
            self.a = 0
            self.clock.tick(self.frame_rate)

    def save_and_menu(self):  # функция, сохраняющая игру и выходящая в меню
        Save_Game(self.current_state_index, self.flags)
        self.current_state_index = self.first_current_state_index
        self.flags = self.first_flags
        self.current_state = self.first_current_state
        self.a = 1
        self.run_menu()


class Button:
    def __init__(self, x, y, w, h, on_click, text, i):
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.on_click = on_click
        self.i = i
        self.text = text
        self.state = 'normal'  # or pressed
        if self.text != '':
            self.font = pygame.font.SysFont('Arial', 20)

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, (self.x, self.y, self.w, self.h))
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


class ButtonMenu:
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


class ButtonSave:
    def __init__(self, x, y, w, h, on_click, text, a, b):
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.on_click = on_click
        self.a = a
        self.b = b
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
            self.on_click(self.a, self.b)
            self.state = 'normal'

    @property
    def back_color(self):
        return dict(normal=(200, 200, 200),
                    pressed=(128, 128, 128))[self.state]


"""определяем имя архива"""
archive = zipfile.ZipFile('resources.zip', 'r')  # создает объект архива
"""создаем массив флагов и заполняем его"""
flags = Flag(3)  # массив флагов
flags.items[0] = 1

global_flags = Flag(2)  # массив глобальных флагов

game = Game(flags)
slide = [0] * 100  # массив всех слайдов
options = [0] * 100  # массив всех массивов опций-

slide[5] = State('5', [(pygame.image.load(ex("slide_4/characters/character.png")), (-100, -650))],
                 pygame.transform.scale(pygame.image.load(ex("slide_4/background.jpg")), (WIDTH, HEIGHT)), [])
options[3] = [Option('дам', game, 5, 5, 1, 2, slide), Option('нетв', game, 5, 5, 1, 2, slide)]

slide[4] = State('4', [(pygame.image.load(ex("slide_2/characters/character.png")), (0, 0))],
                 pygame.transform.scale(pygame.image.load(ex("slide_1/background.jpg")), (WIDTH, HEIGHT)), options[3])
slide[3] = State('3', [(pygame.image.load(ex("slide_3/characters/character.png")), (0, 0))],
                 pygame.transform.scale(pygame.image.load(ex("slide_3/background.jpg")), (WIDTH, HEIGHT)), options[3])

options[2] = [Option('да', game, 3, 4, 1, 2, slide), Option('нет', game, 4, 3, 1, 2, slide),
              Option('минет', game, 4, 3, 1, 2, slide)]
slide[2] = State('2', [(pygame.image.load(ex("slide_2/characters/character.png")), (0, 0))],
                 pygame.transform.scale(pygame.image.load(ex("slide_2/background.jpg")), (WIDTH, HEIGHT)), options[2])

options[1] = [Option('да', game, 2, 2, 0, 1, slide), Option('нет', game, 2, 2, 0, 0, slide)]
slide[1] = State('1', [(pygame.image.load(ex("slide_1/characters/character.png")), (0, 0))],
                 pygame.transform.scale(pygame.image.load(ex("slide_1/background.jpg")), (WIDTH, HEIGHT)), options[1])

game.initialization(slide, 1)
game.run_menu()
