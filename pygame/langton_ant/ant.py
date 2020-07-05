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

    def run(self):
        x = int(self.width_cell_count / 2)
        y = int(self.height_cell_count / 2)

        while self.is_executing:
            print(x, y)

            # Цвет текущей клетки
            current_cell_color = self.board.get_cell_color(x, y)

            # Обновляем цвет на противоположный
            color = self.get_new_color(current_cell_color)

            pygame.draw.rect(self.screen, color, (
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size
            ))
            pygame.display.flip()

            # Исходя из текущего цвета (current_cell_color) определяем, куда поворачивать.
            turn = self.get_new_turn(current_cell_color)

            self.board.set_cell_color(x, y, color)

            # Обновляем координаты
            x, y = self.get_new_position(x, y, turn)

            # Обновляем координаты
            self.direction = self.get_new_direction(turn)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_executing = False

            time.sleep(0.5)

        pygame.quit()

    def get_new_color(self, color):
        if color == Color.WHITE:
            return Color.BLACK
        elif color == Color.BLACK:
            return Color.WHITE
        else:
            raise ValueError('Incorrect color!')

    def get_new_turn(self, color):
        if color == Color.WHITE:
            return Turn.RIGHT
        elif color == Color.BLACK:
            return Turn.LEFT
        else:
            raise ValueError('Incorrect color!')

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


def main():
    pygame.init()

    game = Game()
    game.run()

    pygame.quit()


if __name__ == '__main__':
    main()
