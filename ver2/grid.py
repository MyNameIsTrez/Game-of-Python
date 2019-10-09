import pygame


# def tuple_mult(tup, val):
# return tuple(x*val for x in tup)

class Grid:
    def __init__(self, cols, rows, cell_size, font, screen):
        self.size = (cols, rows)
        self.cell_size = cell_size
        self.font = font
        self.screen = screen
        # self.cell_neighbors

    def create_cells(self, cell_size):
        # create a 2D-array filled with Falses, to hold the cells in an x, y format
        self.cells = [
            [False for row in range(self.size[1])] for col in range(self.size[0])
        ]

        self.cells[0][1] = True
        self.cells[1][2] = True
        self.cells[2][2] = True
        self.cells[2][1] = True
        self.cells[2][0] = True

    def create_cell_neighbors(self, cell_size):
        # create a 2D-array filled with Falses, to hold the cells in an x, y format
        self.cell_neighbors = [
            [0 for row in range(self.size[1])] for col in range(self.size[0])
        ]

    def create_update_list(self):
        # create a 2D-array filled with Falses, to hold the cells in an x, y format
        self.update_list = [
            [False for row in range(self.size[1])] for col in range(self.size[0])
        ]

        for col in range(len(self.cells)):
            for row in range(len(self.cells[col])):
                if (self.cells[col][row]):
                    # set itself to True in update_list
                    self.update_list[col][row] = True
                    # add its neighbors to update_list
                    self.add_neighbor_to_update_list(col, row)

    def add_neighbor_to_update_list(self, col, row):
        top_edge = row == 0
        bottom_edge = row == self.size[1] - 1
        left_edge = col == 0
        right_edge = col == self.size[0] - 1

        # top-left
        if (not top_edge and not left_edge):
            self.update_list[col-1][row-1] = True
        # top
        if (not top_edge):
            self.update_list[col][row-1] = True
        # top-right
        if (not top_edge and not right_edge):
            self.update_list[col+1][row-1] = True
        # left
        if (not left_edge):
            self.update_list[col-1][row] = True
        # right
        if (not right_edge):
            self.update_list[col+1][row] = True
        # bottom-left
        if (not bottom_edge and not left_edge):
            self.update_list[col-1][row+1] = True
        # bottom
        if (not bottom_edge):
            self.update_list[col][row+1] = True
        # bottom-right
        if (not bottom_edge and not right_edge):
            self.update_list[col+1][row+1] = True

    def update_from_update_list(self, ):
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                if (self.update_list[col][row]):
                    neighbors = self.get_neighbor_count(col, row)
                    self.cell_neighbors[col][row] = neighbors

        self.update_cells_state(col, row)

    def get_neighbor_count(self, col, row):
        top_edge = row == 0
        bottom_edge = row == self.size[1] - 1
        left_edge = col == 0
        right_edge = col == self.size[0] - 1

        neighbors = 0

        # top-left
        if (not top_edge and not left_edge):
            neighbors += self.cells[col-1][row-1]
        # top
        if (not top_edge):
            neighbors += self.cells[col][row-1]
        # top-right
        if (not top_edge and not right_edge):
            neighbors += self.cells[col+1][row-1]
        # left
        if (not left_edge):
            neighbors += self.cells[col-1][row]
        # right
        if (not right_edge):
            neighbors += self.cells[col+1][row]
        # bottom-left
        if (not bottom_edge and not left_edge):
            neighbors += self.cells[col-1][row+1]
        # bottom
        if (not bottom_edge):
            neighbors += self.cells[col][row+1]
        # bottom-right
        if (not bottom_edge and not right_edge):
            neighbors += self.cells[col+1][row+1]

        return neighbors

    def draw_neighbor_count(self):
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                if (self.update_list[col][row]):
                    neighbors = self.get_neighbor_count(col, row)

                    pos = (col * self.cell_size + 0.5 * self.cell_size,
                           row * self.cell_size + 0.5 * self.cell_size)
                    self.font.render_to(
                        self.screen, pos, str(neighbors), (255, 50, 50))

    def update_cells_state(self, col, row):
        # switcher = {
        #     2: self.cells[col][row],
        #     3: True,
        # }
        # self.cells[col][row] = switcher.get(neighbors, False)
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                neighbors = self.cell_neighbors[col][row]
                if (neighbors == 3):
                    self.cells[col][row] = True
                elif (neighbors != 2):
                    self.cells[col][row] = False

    def draw_cell_updates(self):
        # we have to use range(len()) to get the index
        for col in range(len(self.update_list)):
            for row in range(len(self.update_list[col])):
                if (self.update_list[col][row]):
                    pygame.draw.rect(
                        self.screen, (255, 255, 255),  # white
                        (col * self.cell_size,  # x
                         row * self.cell_size,  # y
                         self.cell_size, self.cell_size),  # width, height
                        0  # thickness, 0 means fill it instead
                    )

    def draw_cells(self):
        # we have to use range(len()) to get the index
        for col in range(len(self.cells)):
            for row in range(len(self.cells[col])):
                if (self.cells[col][row]):
                    pygame.draw.rect(
                        self.screen, (255, 255, 255),  # white
                        (col * self.cell_size,  # x
                         row * self.cell_size,  # y
                         self.cell_size, self.cell_size),  # width, height
                        0  # thickness, 0 means fill it instead
                    )
