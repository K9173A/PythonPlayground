

import sys

import pygame

from board import Board


pygame.init()


def main():
    board = Board()
    board.run()
    # board.generate_random_board_to_file()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
