"""placeholder"""
import pygame


class Grid:
    """placeholder"""

    def __init__(self, cols, rows, cell_size, font_neighbor, screen):
        self.size = (cols, rows)
        self.cell_size = cell_size
        self.font_neighbor = font_neighbor
        self.screen = screen
        self.cells = None
        self.cell_neighbors = None
        self.update_list = None

    def create_cells(self):
        """placeholder"""
        # create a 2D-array filled with Falses, to hold the cells in an x, y format
        self.cells = [
            [False for row in range(self.size[1])] for col in range(self.size[0])
        ]

        offset = 50

        # r_pentomino
        self.cells[0+offset][1+offset] = True
        self.cells[1+offset][0+offset] = True
        self.cells[1+offset][1+offset] = True
        self.cells[1+offset][2+offset] = True
        self.cells[2+offset][0+offset] = True

        # glider
        # self.cells[0+offset][1+offset] = True
        # self.cells[1+offset][2+offset] = True
        # self.cells[2+offset][2+offset] = True
        # self.cells[2+offset][1+offset] = True
        # self.cells[2+offset][0+offset] = True

    def create_cell_neighbors(self):
        """placeholder"""
        # create a 2D-array filled with Falses, to hold the cells in an x, y format
        self.cell_neighbors = [
            [0 for row in range(self.size[1])] for col in range(self.size[0])
        ]

    def create_update_list(self):
        """placeholder"""
        # create a 2D-array filled with Falses, to hold the cells in an x, y format
        self.update_list = [
            [False for row in range(self.size[1])] for col in range(self.size[0])
        ]

        for col in range(len(self.cells)):
            for row in range(len(self.cells[col])):
                if self.cells[col][row]:
                    # set itself to True in update_list
                    self.update_list[col][row] = True
                    # add its neighbors to update_list
                    self.add_neighbor_to_update_list(col, row)

    def add_neighbor_to_update_list(self, col, row):
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

    def update_from_update_list(self, ):
        """placeholder"""
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                if self.update_list[col][row]:
                    neighbors = self.get_neighbor_count(col, row)
                    self.cell_neighbors[col][row] = neighbors

        self.update_cells_state(col, row)

    def get_neighbor_count(self, col, row):
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

    def draw_neighbor_count(self):
        """placeholder"""
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                if self.update_list[col][row]:
                    neighbors = self.get_neighbor_count(col, row)

                    pos = (col * self.cell_size + 0.5 * self.cell_size,
                           row * self.cell_size + 0.5 * self.cell_size)
                    self.font_neighbor.render_to(
                        self.screen, pos, str(neighbors), (255, 50, 50))

    def update_cells_state(self, col, row):
        """placeholder"""
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                neighbors = self.cell_neighbors[col][row]
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
                        0  # thickness, 0 means fill it instead
                    )
