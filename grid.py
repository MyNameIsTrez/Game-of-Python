import pygame

from cell import Cell


class Grid:
    def __init__(self, cols, rows, cell_size, screen):
        self.set_size(cols, rows)
        self.create_cells(screen, cell_size)

    def set_size(self, cols, rows):
        self.size = (cols, rows)

    def create_cells(self, screen, cell_size):
        # create a matrix to hold the cells in an x, y format
        self.cells = [
            [Cell(col, row, cell_size, screen) for row in range(self.size[1])] for col in range(self.size[0])
        ]

    def draw_cells(self):
        for col in self.cells:
            for cell in col:
                cell.draw()
