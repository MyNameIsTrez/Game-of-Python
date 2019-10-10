from cell import Cell


def tuple_mult(tup, val):
    return tuple(x*val for x in tup)


class Grid:
    def __init__(self, cols, rows, cell_size, screen):
        self.size = (cols, rows)
        self.cell_size = cell_size

        self.create_cells(cell_size, screen)

    def create_cells(self, cell_size, screen):
        # create a 2D-array to hold the cells in
        self.cells = [
            [Cell(col, row, cell_size, screen) for row in range(self.size[1])] for col in range(self.size[0])
        ]

    def calc_cells_neighbors(self):
        for col in self.cells:
            for cell in col:
                cell.count_neighbors(self.cells, self.size)

    def update_cells(self):
        for col in self.cells:
            for cell in col:
                self.update_state(cell)

    def update_state(self, cell):
        switcher = {
            2: cell.alive,
            3: True,
        }
        cell.alive = switcher.get(cell.neighbors, False)

    def draw_cells(self, screen, font):
        for col in self.cells:
            for cell in col:
                cell.draw()
                # text = str(cell.neighbors)
                # font.render_to(screen, tuple_mult(cell.pos, self.cell_size), text,
                #                (60, 205, 150))  # display text
