import pygame

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Rocket:
    # ширина и высота у всех
    # экземпляров-ракет будут одинаковы
    width_rocket = 20
    height_rocket = 50

    def __init__(self, surface, color):
        """Конструктору необходимо передать поверхность, по которой
        будет летать ракета и цвет самой ракеты"""
        self.surf = surface
        self.color = color
        # Методы поверхности get_width() и get_height() возвращают ее размеры.
        # Координаты верхнего левого угла ракеты устанавливаются так,
        # чтобы ракета летела ровно по центру поверхности по горизонтали
        # и появлялась снизу.
        self.x = surface.get_width() // 2 - Rocket.width_rocket // 2
        self.y = surface.get_height()

    def fly(self):
        """Вызов метода fly() поднимает ракету на 3 пикселя.
        Если ракета скрывается вверху, она снова появится снизу"""
        pygame.draw.rect(self.surf, self.color, (self.x, self.y,
                                                 Rocket.width_rocket, Rocket.height_rocket))
        self.y -= 3
        # Если координата y ракеты уходит за -50, то значит она
        # полностью скрылась вверху.
        if self.y < -Rocket.height_rocket:
            # Поэтому перебрасываем ракету под нижнюю границу окна.
            self.y = WIN_HEIGHT


sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# левая белая поверхность, равная половине окна
surf_left = pygame.Surface((WIN_WIDTH // 2, WIN_HEIGHT))
surf_left.fill(WHITE)

# правая черная поверхность, равная другой половине окна
surf_right = pygame.Surface((WIN_WIDTH // 2, WIN_HEIGHT))

# размещаем поверхности на главной, указывая координаты
# их верхних левых углов
sc.blit(surf_left, (0, 0))
sc.blit(surf_right, (WIN_WIDTH // 2, 0))

# создаем черную ракету для левой поверхности
# и белую - для правой
rocket_left = Rocket(surf_left, BLACK)
rocket_right = Rocket(surf_right, WHITE)

# какая половина активна, до первого клика - никакая
active_left = False
active_right = False

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.MOUSEBUTTONUP:
            # если координата X клика меньше половины окна,
            # т. е. клик произошел в левой половине ...
            if i.pos[0] < WIN_WIDTH // 2:
                # то активируем левую, отключаем правую
                active_left = True
                active_right = False
            elif i.pos[0] > WIN_WIDTH // 2:
                # иначе - наоборот
                active_right = True
                active_left = False

    if active_left:
        # Если активна левая поверхность,
        # то заливаем только ее цветом,
        surf_left.fill(WHITE)
        # поднимаем ракету,
        rocket_left.fly()
        # заново отрисовываем левую поверхность на главной.
        sc.blit(surf_left, (0, 0))
    elif active_right:
        # Если активна правая -> аналогично
        surf_right.fill(BLACK)
        rocket_right.fly()
        sc.blit(surf_right, (WIN_WIDTH // 2, 0))

    pygame.display.update()

    pygame.time.delay(20)