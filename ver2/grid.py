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
        self.cells_list = None
        self.neighbor_count_list = None
        self.update_list = None
        self.starter_cells_blueprint = starter_cells_blueprint

    def create_cells_list(self):
        """makes a 2D array called cells_list, and fills it with Falses"""
        # create a 2D array filled with Falses, to hold the states of the cells_list in
        self.cells_list = [
            [False for row in range(self.size[1])] for col in range(self.size[0])
        ]

    def set_starter_cells_list(self):
        """sets some of the cells_list to True, according to r_pentomino/glider"""
        offset_x = math.floor(self.size[0] / 2)
        offset_y = math.floor(self.size[1] / 2)

        if self.starter_cells_blueprint == 1:
            # r_pentomino
            self.cells_list[0+offset_x][1+offset_y] = True
            self.cells_list[1+offset_x][0+offset_y] = True
            self.cells_list[1+offset_x][1+offset_y] = True
            self.cells_list[1+offset_x][2+offset_y] = True
            self.cells_list[2+offset_x][0+offset_y] = True
        else:
            # glider, useful for seeing if the cell states are being set incorrectly
            self.cells_list[0+offset_x][1+offset_y] = True
            self.cells_list[1+offset_x][2+offset_y] = True
            self.cells_list[2+offset_x][2+offset_y] = True
            self.cells_list[2+offset_x][1+offset_y] = True
            self.cells_list[2+offset_x][0+offset_y] = True

    def create_update_list(self):
        """(re)makes an empty 1D array for storing the cells_list that are alive, and their neighbors"""
        self.update_list = []

    def set_update_list(self):
        """sets alive cells_list and their (dead) neighbors to True in update_list"""
        for col in range(len(self.cells_list)):
            for row in range(len(self.cells_list[col])):
                if self.cells_list[col][row]:
                    # adds itself to update_list
                    self.update_list.append((col, row))
                    # adds its neighbors to update_list
                    self.set_neighbor_to_update_list(col, row)
        # removes all duplicate entries
        self.update_list = list(set(self.update_list))

    def set_neighbor_to_update_list(self, col, row):
        """placeholder"""
        top_edge = row == 0
        bottom_edge = row == self.size[1] - 1
        left_edge = col == 0
        right_edge = col == self.size[0] - 1

        # top-left
        if (not top_edge and not left_edge):
            self.update_list.append((col-1, row-1))
        # top
        if not top_edge:
            self.update_list.append((col, row-1))
        # top-right
        if not top_edge and not right_edge:
            self.update_list.append((col+1, row-1))
        # left
        if not left_edge:
            self.update_list.append((col-1, row))
        # right
        if not right_edge:
            self.update_list.append((col+1, row))
        # bottom-left
        if not bottom_edge and not left_edge:
            self.update_list.append((col-1, row+1))
        # bottom
        if not bottom_edge:
            self.update_list.append((col, row+1))
        # bottom-right
        if (not bottom_edge and not right_edge):
            self.update_list.append((col+1, row+1))

    def create_neighbor_count_list(self):
        # """(re)makes an empty 1D array for storing the cells_list that have a neighbor count"""
        # self.neighbor_count_list = []
        """(re)makes a 2D array with a neighbor count of 0 for each cell"""
        self.neighbor_count_list = [
            [0 for row in range(self.size[1])] for col in range(self.size[0])
        ]

    def set_neighbor_count_list_list(self):
        """uses update_list to update the neighbor count array"""
        for pos in self.update_list:
            neighbors = self.get_neighbor_count_list(pos[0], pos[1])
            self.neighbor_count_list[pos[0]][pos[1]] = neighbors

    def get_neighbor_count_list(self, col, row):
        """placeholder"""
        top_edge = row == 0
        bottom_edge = row == self.size[1] - 1
        left_edge = col == 0
        right_edge = col == self.size[0] - 1

        neighbors = 0

        # top-left
        if (not top_edge and not left_edge):
            neighbors += self.cells_list[col-1][row-1]
        # top
        if not top_edge:
            neighbors += self.cells_list[col][row-1]
        # top-right
        if not top_edge and not right_edge:
            neighbors += self.cells_list[col+1][row-1]
        # left
        if not left_edge:
            neighbors += self.cells_list[col-1][row]
        # right
        if not right_edge:
            neighbors += self.cells_list[col+1][row]
        # bottom-left
        if not bottom_edge and not left_edge:
            neighbors += self.cells_list[col-1][row+1]
        # bottom
        if not bottom_edge:
            neighbors += self.cells_list[col][row+1]
        # bottom-right
        if (not bottom_edge and not right_edge):
            neighbors += self.cells_list[col+1][row+1]

        return neighbors

    def set_cells_state(self):
        """uses update_list to change the cell array"""
        for pos in self.update_list:
            neighbors = self.neighbor_count_list[pos[0]][pos[1]]
            if neighbors == 3:
                self.cells_list[pos[0]][pos[1]] = True
            elif neighbors != 2:
                self.cells_list[pos[0]][pos[1]] = False

    def draw_cells(self):
        """placeholder"""
        # we have to use range(len()) to get the index
        for col in range(len(self.cells_list)):
            for row in range(len(self.cells_list[col])):
                if self.cells_list[col][row]:
                    pygame.draw.rect(
                        self.screen, (255, 255, 255),  # white
                        (col * self.cell_size,  # x
                         row * self.cell_size,  # y
                         self.cell_size, self.cell_size),  # width, height
                        0  # thickness, 0 means fill instead
                    )

    def draw_neighbor_count_list_bool(self):
        """placeholder"""
        for pos in self.update_list:
            neighbors = self.get_neighbor_count_list(pos[0], pos[1])

            coords = (pos[0] * self.cell_size + 0.5 * self.cell_size,
                      pos[1] * self.cell_size + 0.5 * self.cell_size)
            self.font_neighbor.render_to(
                self.screen, coords, str(neighbors), (255, 50, 50))

    def draw_updated_cells(self):
        """placeholder"""
        for pos in self.update_list:
            pygame.draw.rect(
                self.screen, (255, 0, 0),  # red
                (pos[0] * self.cell_size,  # x
                 pos[1] * self.cell_size,  # y
                 self.cell_size, self.cell_size),  # width, height
                0  # thickness, 0 means fill instead
            )
