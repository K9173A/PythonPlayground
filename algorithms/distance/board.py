
import functools
import os
import random
import time
from dataclasses import dataclass
from queue import Queue
from typing import Callable, List, Tuple, Union


import pygame
from pygame.locals import DOUBLEBUF


class CellCategory:
    BLOCK = 0
    FREE_AREA = 1
    START = 2
    FINISH = 3
    CURRENTLY_VISITED = 4
    PREVIOUSLY_VISITED = 5
    SHORTEST_PATH = 6


@dataclass
class Cell:
    x: int
    y: int
    category: int

    def __hash__(self) -> int:
        return hash(self.id_)

    @property
    def id_(self) -> int:
        return self.y * 100 + self.x


@dataclass(frozen=True)
class Edge:
    first_cell: Cell
    second_cell: Cell

    def get_other_cell(self, this_cell: Cell) -> Union[Cell, None]:
        if this_cell.id_ == self.first_cell.id_:
            return self.second_cell
        elif this_cell.id_ == self.second_cell.id_:
            return self.first_cell
        else:
            return None


def timer(func):
    @functools.wraps(func)
    def wrapped(self, *args, **kwargs):
        start_ts = time.time()
        func(self, *args, **kwargs)
        end_ts = time.time()
        delta = end_ts - start_ts
        print(f'{func.__name__} took {delta} secs to execute')
    return wrapped


def rect(x, y) -> Tuple[int, int, int, int]:
    return (x * Board.cell_size_px,
            y * Board.cell_size_px,
            Board.cell_size_px,
            Board.cell_size_px)


def generate_random_board_to_file() -> None:
    now_ts = time.time()
    path = os.path.join(os.path.dirname(__file__), f'board-{now_ts}.txt')

    lines = ''
    probabilities = ''.join([k * v for k, v in {'+': 70, '#': 30}.items()])
    for _ in range(Board.cell_count):
        for _ in range(Board.cell_count):
            lines += probabilities[random.randint(a=0, b=99)]
        lines += '\n'

    with open(file=path, mode='w', encoding='utf-8') as f:
        f.write(lines)


class Graph:
    def __init__(self, cells: List[List[Cell]]):
        self._edges = []

        # horizontal edges
        for cells_row in cells:
            self.prepare_edges(cells_row)

        # vertical edges
        for i in range(len(cells)):
            self.prepare_edges([cells_row[i] for cells_row in cells])

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        neighbors = []

        for edge in self._edges[:]:
            neighbor_cell = edge.get_other_cell(cell)
            if (
                    neighbor_cell
                    and neighbor_cell.category in [CellCategory.FREE_AREA, CellCategory.FINISH]
                    and neighbor_cell not in neighbors
            ):
                neighbors.append(neighbor_cell)
                self._edges.remove(edge)

        return neighbors

    @staticmethod
    def is_visitable_cell(cell: Cell) -> bool:
        return cell.category in [CellCategory.FREE_AREA, CellCategory.START, CellCategory.FINISH]

    def prepare_edges(self, cells: List[Cell]):
        left_cell_index = 0
        right_cell_index = left_cell_index + 1

        while right_cell_index < len(cells):
            left_cell = cells[left_cell_index]
            right_cell = cells[right_cell_index]

            if self.is_visitable_cell(left_cell) and self.is_visitable_cell(right_cell):
                # We assume that we don't need to check the same cell twice, otherwise it would be
                # required to spend time checking `Edge` existence in the `self,_edges`
                self._edges.append(Edge(first_cell=left_cell, second_cell=right_cell))

            left_cell_index += 1
            right_cell_index += 1


class Finished(RuntimeError):
    pass


class Board:

    cell_size_px = 8
    cell_count = 100

    symbol_to_cell_category_mapper = {
        '#': CellCategory.BLOCK,
        '+': CellCategory.FREE_AREA,
        'S': CellCategory.START,
        'F': CellCategory.FINISH,
        'C': CellCategory.CURRENTLY_VISITED,
        'P': CellCategory.PREVIOUSLY_VISITED
    }

    cell_category_to_color_mapper = {
        CellCategory.BLOCK: (50, 50, 50),
        CellCategory.FREE_AREA: (150, 150, 150),
        CellCategory.START: (0, 255, 0),
        CellCategory.FINISH: (255, 0, 0),
        CellCategory.CURRENTLY_VISITED: (0, 75, 255),
        CellCategory.PREVIOUSLY_VISITED: (0, 75, 150),
        CellCategory.SHORTEST_PATH: (0, 255, 255)
    }

    def __init__(self) -> None:
        total_size_px = Board.cell_size_px * Board.cell_count
        path = os.path.join(os.path.dirname(__file__), 'board-1637527679.5008295.txt')

        self._clock = pygame.time.Clock()
        self._window = pygame.display.set_mode((total_size_px, total_size_px), DOUBLEBUF)
        self._surface = pygame.Surface((total_size_px, total_size_px))

        self._cells_matrix = []
        self._start_cell = None
        self._finish_cell = None

        with open(file=path, mode='r', encoding='utf-8') as f:
            for y, line in enumerate(f.readlines()):
                cells_row = []
                for x, char in enumerate(line.strip()):
                    cell = Cell(x, y, Board.symbol_to_cell_category_mapper[char])
                    if Board.symbol_to_cell_category_mapper[char] == CellCategory.START:
                        self._start_cell = cell
                    elif Board.symbol_to_cell_category_mapper[char] == CellCategory.FINISH:
                        self._finish_cell = cell
                    cells_row.append(cell)
                self._cells_matrix.append(cells_row)

        self._graph = Graph(self._cells_matrix)
        self._frontier = Queue()
        self._frontier.put(self._start_cell)
        self._came_from = {self._start_cell: None}  # source -> destination

        # Limit allowed events for optimization purposes
        pygame.event.set_allowed([pygame.QUIT])
        self._window.set_alpha(None)

    def run(self) -> None:
        self.__init_board()
        try:
            self.__run(self.a_star)
            self.__run(self.display_shortest_path)
            self.__run(self.idle)
        except SystemExit:
            pass

    def __init_board(self):
        for cells_row in self._cells_matrix:
            for cell in cells_row:
                self._surface.fill(self.cell_category_to_color_mapper[cell.category], rect(cell.x, cell.y))

        self._window.blit(self._surface, (0, 0))
        pygame.display.flip()

    def __run(self, func: Callable) -> None:
        while True:
            self._clock.tick(60)
            self.handle_events()

            start_ts = time.time()
            try:
                func()
            except Finished:
                break
            finally:
                end_ts = time.time()
                delta = end_ts - start_ts
                print(f'{func.__name__} took {delta} secs to execute')

    def a_star(self):
        if self._frontier.empty():
            return

        stop = False
        rects = []

        # Amount of iterations was determined via experiments. The bigger number, the lesser execution time.
        # However after 20 it does not influence much, as we obviously reached the limit.
        # This number defines how many cells we update in one a_star cycle (in one frame).
        for _ in range(20):
            current_cell = self._frontier.get()

            for next_neighbor_cell in self._graph.get_neighbors(current_cell):
                if next_neighbor_cell.category == CellCategory.FINISH:
                    stop = True
                else:
                    next_neighbor_cell.category = CellCategory.CURRENTLY_VISITED

                if current_cell.category != CellCategory.START:
                    current_cell.category = CellCategory.PREVIOUSLY_VISITED

                self._frontier.put(next_neighbor_cell)
                self._came_from[next_neighbor_cell] = current_cell

                rects.extend([
                    self.display_cell(next_neighbor_cell),
                    self.display_cell(current_cell)
                ])

                if stop:
                    raise Finished

        # Render only updated cells
        if rects:
            pygame.display.update(rects)

    def display_shortest_path(self) -> None:
        """
        Traverses through the graph of cells in a reversed order (from destination to the source).
        Any destination is guaranteed to have only one source, so eventually we will reach the start cell.
        """
        current_cell = self._finish_cell

        while True:
            try:
                previous_cell = self._came_from[current_cell]
            except KeyError:
                break  # Start cell does not have any source

            if previous_cell and previous_cell.category != CellCategory.START:
                    previous_cell.category = CellCategory.SHORTEST_PATH
                    pygame.display.update(self.display_cell(previous_cell))
                    current_cell = previous_cell
            else:
                break

    def idle(self) -> None:
        """
        After printing the shortest path app keeps running and handles events.
        This method does nothing just to support the signature of __run() method.
        """
        time.sleep(0.5)

    def display_cell(self, cell: Cell) -> Tuple[int, int, int, int]:
        r = rect(cell.x, cell.y)
        pygame.draw.rect(self._window, self.cell_category_to_color_mapper[cell.category], r)
        return r

    @staticmethod
    def handle_events() -> None:
        """
        Handles pressing the [X] button and ESCAPE button to quit the app.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            raise SystemExit
