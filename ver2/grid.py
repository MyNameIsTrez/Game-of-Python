"""placeholder"""
import math

import pygame


class Grid:
    """placeholder"""

    def __init__(self, cols, rows, cell_size, font_neighbor, starter_cells_blueprint, screen):
        self.size = (cols, rows)
        self.cell_size = cell_size
        self.font_neighbor = font_neighbor
        self.screen = screen
        self.cells = None
        self.neighbor_count_list = None
        self.update_list = None
        self.starter_cells_blueprint = starter_cells_blueprint

    def create_cells(self):
        """makes a 2D array called cells, and fills it with Falses"""
        # create a 2D array filled with Falses, to hold the states of the cells in
        self.cells = [
            [False for row in range(self.size[1])] for col in range(self.size[0])
        ]

    def set_starter_cells(self):
        """sets some of the cells to True, according to r_pentomino/glider"""
        offset_x = math.floor(self.size[0] / 2)
        offset_y = math.floor(self.size[1] / 2)

        if self.starter_cells_blueprint == 1:
            # r_pentomino
            self.cells[0+offset_x][1+offset_y] = True
            self.cells[1+offset_x][0+offset_y] = True
            self.cells[1+offset_x][1+offset_y] = True
            self.cells[1+offset_x][2+offset_y] = True
            self.cells[2+offset_x][0+offset_y] = True
        else:
            # glider, useful for seeing if the cell states are being set incorrectly
            self.cells[0+offset_x][1+offset_y] = True
            self.cells[1+offset_x][2+offset_y] = True
            self.cells[2+offset_x][2+offset_y] = True
            self.cells[2+offset_x][1+offset_y] = True
            self.cells[2+offset_x][0+offset_y] = True

    def create_update_list(self):
        # """(re)makes an empty 1D array for storing the cells that are alive, and their neighbors"""
        # self.update_list = []
        """(re)makes a 2D array called update_list, and fills it with Falses"""
        # create a 2D array filled with Falses, to hold the cells in
        self.update_list = [
            [False for row in range(self.size[1])] for col in range(self.size[0])
        ]

    def set_update_list(self):
        """sets alive cells and their (dead) neighbors to True in update_list"""
        for col in range(len(self.cells)):
            for row in range(len(self.cells[col])):
                if self.cells[col][row]:
                    # sets itself to True in update_list
                    self.update_list[col][row] = True
                    # add its neighbors to update_list
                    self.set_neighbor_to_update_list(col, row)

    def set_neighbor_to_update_list(self, col, row):
        """placeholder"""
        top_edge = row == 0
        bottom_edge = row == self.size[1] - 1
        left_edge = col == 0
        right_edge = col == self.size[0] - 1

        # top-left
        if (not top_edge and not left_edge):
            self.update_list[col-1][row-1] = True
        # top
        if not top_edge:
            self.update_list[col][row-1] = True
        # top-right
        if not top_edge and not right_edge:
            self.update_list[col+1][row-1] = True
        # left
        if not left_edge:
            self.update_list[col-1][row] = True
        # right
        if not right_edge:
            self.update_list[col+1][row] = True
        # bottom-left
        if not bottom_edge and not left_edge:
            self.update_list[col-1][row+1] = True
        # bottom
        if not bottom_edge:
            self.update_list[col][row+1] = True
        # bottom-right
        if (not bottom_edge and not right_edge):
            self.update_list[col+1][row+1] = True

    def create_neighbor_count_list(self):
        # """(re)makes an empty 1D array for storing the cells that have a neighbor count"""
        # self.neighbor_count_list = []
        """(re)makes a 2D array with a neighbor count of 0 for each cell"""
        # (re)makes a 2D array with a neighbor count of 0 for each cell
        self.neighbor_count_list = [
            [0 for row in range(self.size[1])] for col in range(self.size[0])
        ]

    def set_neighbor_count_list_list(self):
        """uses update_list to update the neighbor count array"""
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                if self.update_list[col][row]:
                    # gets and then sets the number of alive neighbors around this cell
                    neighbors = self.get_neighbor_count_list(col, row)
                    self.neighbor_count_list[col][row] = neighbors

    def get_neighbor_count_list(self, col, row):
        """placeholder"""
        top_edge = row == 0
        bottom_edge = row == self.size[1] - 1
        left_edge = col == 0
        right_edge = col == self.size[0] - 1

        neighbors = 0

        # top-left
        if (not top_edge and not left_edge):
            neighbors += self.cells[col-1][row-1]
        # top
        if not top_edge:
            neighbors += self.cells[col][row-1]
        # top-right
        if not top_edge and not right_edge:
            neighbors += self.cells[col+1][row-1]
        # left
        if not left_edge:
            neighbors += self.cells[col-1][row]
        # right
        if not right_edge:
            neighbors += self.cells[col+1][row]
        # bottom-left
        if not bottom_edge and not left_edge:
            neighbors += self.cells[col-1][row+1]
        # bottom
        if not bottom_edge:
            neighbors += self.cells[col][row+1]
        # bottom-right
        if (not bottom_edge and not right_edge):
            neighbors += self.cells[col+1][row+1]

        return neighbors

    def set_cells_state(self):
        """uses update_list to change the cell array"""
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                neighbors = self.neighbor_count_list[col][row]
                if neighbors == 3:
                    self.cells[col][row] = True
                elif neighbors != 2:
                    self.cells[col][row] = False

    def draw_cells(self):
        """placeholder"""
        # we have to use range(len()) to get the index
        for col in range(len(self.cells)):
            for row in range(len(self.cells[col])):
                if self.cells[col][row]:
                    pygame.draw.rect(
                        self.screen, (255, 255, 255),  # white
                        (col * self.cell_size,  # x
                         row * self.cell_size,  # y
                         self.cell_size, self.cell_size),  # width, height
                        0  # thickness, 0 means fill instead
                    )

    def draw_neighbor_count_list_bool(self):
        """placeholder"""
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                if self.update_list[col][row]:
                    neighbors = self.get_neighbor_count_list(col, row)

                    pos = (col * self.cell_size + 0.5 * self.cell_size,
                           row * self.cell_size + 0.5 * self.cell_size)
                    self.font_neighbor.render_to(
                        self.screen, pos, str(neighbors), (255, 50, 50))

    def draw_updated_cells(self):
        """placeholder"""
        # we have to use range(len()) to get the index
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                if self.update_list[col][row]:
                    pygame.draw.rect(
                        self.screen, (255, 0, 0),  # red
                        (col * self.cell_size,  # x
                         row * self.cell_size,  # y
                         self.cell_size, self.cell_size),  # width, height
                        0  # thickness, 0 means fill instead
                    )
