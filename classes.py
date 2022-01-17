import pygame


class Field:
    # сам класс доски. дальше опишу подробно каждый метод
    def __init__(self, width, height, colors, cell_size, boarders):
        self.boarders = boarders  # отступы
        self.field = [[Cell(colors, i, j) for i in range(width)] for j in range(height)]
        self.width, self.height = width, height  # кол-во клеток на поле
        self.colors = colors  # colors = (dead cell color, alive cell color)
        self.cell_size = cell_size  # сторона клетки в пикселях

    def step(self, screen, ongoing):
        """весь процесс (расчет + отрисовка) совершения одного шага в игре. смерть/рождение клеток"""
        new_field = [[Cell(self.colors, i, j) for i in range(self.width)] for j in range(self.height)]

        for j in range(self.height):
            for i in range(self.width):
                cur = self.field[j][i]  # текущая клетка
                pygame.draw.rect(screen, cur.color,
                                 (self.boarders[0] + i * self.cell_size+1, self.boarders[1] + j * self.cell_size+1,
                                  self.cell_size-1, self.cell_size))  # рисуем саму клетку
                count = self.get_count(i, j)  # кол-во живых соседов клетки
                # определяем ее дальнейшую судьбу
                if ongoing:
                    if count in (2, 3) and cur.is_alive() or count == 3 and not cur.is_alive():
                        new_field[j][i].set_alive(1, self.colors)
                    else:
                        new_field[j][i].set_alive(0, self.colors)

                if j == 0:
                    self.draw_vert(screen, i)  # вертикали сразу же рисуем только на j == 0

            self.draw_hor(screen, j)  # рисуем также и горизонтали

        # нужно нарисовать еще одну вертикаль и горизонталь
        # (тк их на одну больше, чем ширина и длина поля соответственно)
        self.draw_vert(screen, self.width)
        self.draw_hor(screen, self.height)
        if ongoing:
            self.field = new_field

    def draw_hor(self, screen, j, grid_color=pygame.Color('white')):
        """рисуем горизонталь"""
        pygame.draw.line(screen, grid_color, (self.boarders[0], self.boarders[1] + j * self.cell_size),
                         (self.boarders[0] + self.width * self.cell_size, self.boarders[1] + j * self.cell_size))

    def draw_vert(self, screen, i, grid_color=pygame.Color('white')):
        """рисуем вертикаль"""
        pygame.draw.line(screen, grid_color, (self.boarders[0] + i * self.cell_size, self.boarders[1]),
                         (self.boarders[0] + i * self.cell_size, self.boarders[1] + self.height * self.cell_size))

    def get_count(self, x, y):
        """метод, определяющий кол-во живых соседей у клетки xy"""
        a = sum((self.field[(y + j) % self.height][(x + i) % self.width].is_alive()
                for i in [-1, 0, 1] for j in [-1, 0, 1])) - self.field[y][x].is_alive()
        return a


class Cell:
    # класс, реализующий одну клетку
    def __init__(self, colors, x, y):
        self.alive = 0
        self.color = colors[0]
        self.coors = x, y

    def is_alive(self):
        """возвращает 1, если клетка живая, 0 - мертвая"""
        return self.alive

    def set_alive(self, value, colors):
        """задает параметр"""
        self.alive = value
        if value == 0:
            self.color = colors[0]
        else:
            self.color = colors[1]

