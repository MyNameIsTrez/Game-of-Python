import pygame
import random


# def tuple_add(tup1, tup2):
#     return tuple(sum(x) for x in zip(tup1, tup2))


def tuple_mult(tup, val):
    return tuple(x*val for x in tup)


black_cell_img = pygame.image.load("images/black_cell.png")
white_cell_img = pygame.image.load("images/white_cell.png")

# get the image width and height as a tuple
cell_rect = white_cell_img.get_rect()


class Cell:
    def __init__(self, col, row, cell_size, screen):
        self.pos = (col, row)
        self.screen = screen
        self.cell_size = cell_size
        # self.alive = random.randint(0, 10) < 3
        if (
            col == 0 and row == 1 or
            col == 1 and row == 2 or
            col == 2 and row == 2 or
            col == 2 and row == 1 or
            col == 2 and row == 0
        ):
            self.alive = True
        else:
            self.alive = False

    def draw(self):
        # draw from the top-left corner of this cell
        if self.alive:
            self.screen.blit(white_cell_img, tuple_mult(
                self.pos, self.cell_size))
        else:
            self.screen.blit(black_cell_img, tuple_mult(
                self.pos, self.cell_size))

    def count_neighbors(self, grid_cells, grid_size):
        top_edge = self.pos[1] == 0
        bottom_edge = self.pos[1] == grid_size[1] - 1
        left_edge = self.pos[0] == 0
        right_edge = self.pos[0] == grid_size[0] - 1

        self.neighbors = 0

        # top-left
        if (not top_edge and not left_edge):
            self.neighbors += grid_cells[self.pos[0]-1][self.pos[1]-1].alive
        # top
        if (not top_edge):
            self.neighbors += grid_cells[self.pos[0]][self.pos[1]-1].alive
        # top-right
        if (not top_edge and not right_edge):
            self.neighbors += grid_cells[self.pos[0]+1][self.pos[1]-1].alive
        # left
        if (not left_edge):
            self.neighbors += grid_cells[self.pos[0]-1][self.pos[1]].alive
        # right
        if (not right_edge):
            self.neighbors += grid_cells[self.pos[0]+1][self.pos[1]].alive
        # bottom-left
        if (not bottom_edge and not left_edge):
            self.neighbors += grid_cells[self.pos[0]-1][self.pos[1]+1].alive
        # bottom
        if (not bottom_edge):
            self.neighbors += grid_cells[self.pos[0]][self.pos[1]+1].alive
        # bottom-right
        if (not bottom_edge and not right_edge):
            self.neighbors += grid_cells[self.pos[0]+1][self.pos[1]+1].alive
