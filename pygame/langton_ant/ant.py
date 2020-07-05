import time
import copy

import pygame


pygame.init()


class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Turn:
    LEFT = 0
    RIGHT = 1


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)


class Board:
    def __init__(self, width, height):
        self.grid = [copy.copy([Color.WHITE] * width) for _ in range(height)]

    def get_cell_color(self, x, y):
        return self.grid[x][y]

    def set_cell_color(self, x, y, color):
        self.grid[x][y] = color


class Game:
    def __init__(self):
        self.cell_size = 5

        self.width_cell_count = 100
        self.height_cell_count = 100

        self.board = Board(self.width_cell_count, self.height_cell_count)

        self.screen = pygame.display.set_mode((
            self.cell_size * self.width_cell_count,
            self.cell_size * self.height_cell_count
        ))
        self.screen.fill(Color.WHITE)

        pygame.display.flip()

        self.is_executing = True

        self.direction = Direction.UP

        self.logic = {
            Color.WHITE: (Turn.LEFT, Color.BLUE),
            Color.BLUE: (Turn.LEFT, Color.RED),
            Color.RED: (Turn.RIGHT, Color.GREEN),
            Color.GREEN: (Turn.LEFT, Color.YELLOW),
            Color.YELLOW: (Turn.RIGHT, Color.WHITE)
        }

    def run(self):
        x = int(self.width_cell_count / 2)
        y = int(self.height_cell_count / 2)

        while self.is_executing:
            # Цвет текущей клетки
            current_cell_color = self.board.get_cell_color(x, y)

            turn, color = self.logic[current_cell_color]

            pygame.draw.rect(self.screen, color, (
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size
            ))
            pygame.display.flip()

            # Исходя из текущего цвета (current_cell_color) определяем, куда поворачивать.
            # turn = self.get_new_turn(current_cell_color)

            self.board.set_cell_color(x, y, color)

            # Обновляем координаты
            x, y = self.check_bounds(*self.get_new_position(x, y, turn))

            # Обновляем координаты
            self.direction = self.get_new_direction(turn)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_executing = False

            time.sleep(0.01)

        pygame.quit()

    def get_new_direction(self, turn):
        new_direction = self.direction

        # Против часовой стрелке - уменьшение значения
        if turn == Turn.LEFT:
            new_direction += 1
            if new_direction > 3:
                new_direction = 0

        # По часовой стрелке - увеличени значения
        elif turn == Turn.RIGHT:
            new_direction -= 1
            if new_direction < 0:
                new_direction = 3
        else:
            raise ValueError('Incorrect turn!')

        return new_direction

    def get_new_position(self, x, y, turn):
        if turn == Turn.LEFT:
            if self.direction == Direction.LEFT:
                return x, y + 1
            elif self.direction == Direction.UP:
                return x - 1, y
            elif self.direction == Direction.RIGHT:
                return x, y - 1
            elif self.direction == Direction.DOWN:
                return x + 1, y
            else:
                raise ValueError('Incorrect direction!')
        elif turn == Turn.RIGHT:
            if self.direction == Direction.LEFT:
                return x, y - 1
            elif self.direction == Direction.UP:
                return x + 1, y
            elif self.direction == Direction.RIGHT:
                return x, y + 1
            elif self.direction == Direction.DOWN:
                return x - 1, y
            else:
                raise ValueError('Incorrect direction!')
        else:
            raise ValueError('Incorrect turn!')

    def check_bounds(self, x, y):
        if x < 0:
            x = self.width_cell_count - 1
        elif x >= self.width_cell_count:
            x = 0

        if y < 0:
            y = self.height_cell_count - 1
        elif y >= self.height_cell_count:
            y = 0

        return x, y


def main():
    pygame.init()

    game = Game()
    game.run()

    pygame.quit()


if __name__ == '__main__':
    main()
