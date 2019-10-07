import pygame

import random


def tuple_add(tup1, tup2):
    return tuple(sum(x) for x in zip(tup1, tup2))


def tuple_mult(tup, val):
    return tuple(x*val for x in tup)


black_cell_img = pygame.image.load("images/black_cell.png")
white_cell_img = pygame.image.load("images/white_cell.png")
# cell_img = pygame.image.load("intro_ball.gif")  # load the texture of the cell

# get the image width and height as a tuple
cell_rect = white_cell_img.get_rect()


class Cell:
    def __init__(self, row, col, cell_size, screen):
        self.set_pos(row * cell_size, col * cell_size)
        self.screen = screen
        self.cell_size = cell_size
        self.alive = random.randint(0, 1)

    def set_pos(self, x, y):
        self.pos = (x, y)

    def draw(self):
        # draw from the top-left corner of this cell
        if self.alive:
            # self.screen.blit(black_cell_img, cell_rect.move(self.pos))
            self.screen.blit(black_cell_img, self.pos)
        else:
            # self.screen.blit(white_cell_img, cell_rect.move(self.pos))
            self.screen.blit(white_cell_img, self.pos)
