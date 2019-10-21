
import math
import random
import time

# from multiprocessing import Pool
# from functools import partial


# def set_self_and_neighbors_to_update_list(grid, cell):
#     col = cell[0]
#     row = cell[1]

#     # adds itself to update_list
#     grid.update_list.append((cell[0], cell[1]))

#     # adds neighbors to update_list
#     top_edge = row == 0
#     bottom_edge = row == grid.size[1] - 1
#     left_edge = col == 0
#     right_edge = col == grid.size[0] - 1

#     # top-left
#     if (not top_edge and not left_edge):
#         grid.update_list.append((col - 1, row - 1))
#     # top
#     if not top_edge:
#         grid.update_list.append((col, row - 1))
#     # top-right
#     if not top_edge and not right_edge:
#         grid.update_list.append((col + 1, row - 1))
#     # left
#     if not left_edge:
#         grid.update_list.append((col - 1, row))
#     # right
#     if not right_edge:
#         grid.update_list.append((col + 1, row))
#     # bottom-left
#     if not bottom_edge and not left_edge:
#         grid.update_list.append((col - 1, row + 1))
#     # bottom
#     if not bottom_edge:
#         grid.update_list.append((col, row + 1))
#     # bottom-right
#     if (not bottom_edge and not right_edge):
#         grid.update_list.append((col + 1, row + 1))


class Grid:

	def __init__(self, cols, rows, cell_size, neighbor_count_color,
              starter_cells_blueprint, random_starter_cells, artist, screen):
		self.size = (cols, rows)
		self.cell_size = cell_size
		self.neighbor_count_color = neighbor_count_color
		self.starter_cells_blueprint = starter_cells_blueprint
		self.random_starter_cells = random_starter_cells
		self.artist = artist
		self.screen = screen

		# makes a 1D array for storing the cols and rows of cells that are alive
		self.cells_list = []
		self.neighbor_count_list = None
		self.update_list = None
		self.total_cell_count = cols * rows
		# self.pool = Pool()

	def set_starter_cells_list(self):
		# adds some cells to cells_list, according to the r_pentomino/glider blueprints
		offset = (math.floor(self.size[0] / 2), math.floor(self.size[1] / 2))

		if self.random_starter_cells:
			for col in range(self.size[0]):
				for row in range(self.size[1]):
					if random.randint(0, 1):
						self.cells_list.append((col, row))
		else:
			if self.starter_cells_blueprint == 1:
				# r_pentomino
				self.cells_list.append((0 + offset[0], 1 + offset[1]))
				self.cells_list.append((1 + offset[0], 0 + offset[1]))
				self.cells_list.append((1 + offset[0], 1 + offset[1]))
				self.cells_list.append((1 + offset[0], 2 + offset[1]))
				self.cells_list.append((2 + offset[0], 0 + offset[1]))
			else:
				# glider
				# useful for checking if the cell states are being set incorrectly
				self.cells_list.append((0 + offset[0], 1 + offset[1]))
				self.cells_list.append((1 + offset[0], 2 + offset[1]))
				self.cells_list.append((2 + offset[0], 2 + offset[1]))
				self.cells_list.append((2 + offset[0], 1 + offset[1]))
				self.cells_list.append((2 + offset[0], 0 + offset[1]))

	def create_update_list(self):
		self.update_list = []

		# utilizing multiprocessing
		# https://stackoverflow.com/a/25553970
		# t1 = time.time()
		# func = partial(set_self_and_neighbors_to_update_list, self)
		# iterable = self.cells_list
		# self.pool.map(func, iterable)
		# t2 = time.time()
		# print("total time: " + str(round(t2 - t1, 4)) + "s")

		for cell in self.cells_list:
			self.set_self_and_neighbors_to_update_list(cell)

		# removes all duplicate entries
		self.update_list = list(set(self.update_list))

	def set_self_and_neighbors_to_update_list(self, cell):
		col = cell[0]
		row = cell[1]

		# adds itself to update_list
		self.update_list.append((cell[0], cell[1]))

		# adds neighbors to update_list
		top_edge = row == 0
		bottom_edge = row == self.size[1] - 1
		left_edge = col == 0
		right_edge = col == self.size[0] - 1

		# top-left
		if (not top_edge and not left_edge):
			self.update_list.append((col - 1, row - 1))
		# top
		if not top_edge:
			self.update_list.append((col, row - 1))
		# top-right
		if not top_edge and not right_edge:
			self.update_list.append((col + 1, row - 1))
		# left
		if not left_edge:
			self.update_list.append((col - 1, row))
		# right
		if not right_edge:
			self.update_list.append((col + 1, row))
		# bottom-left
		if not bottom_edge and not left_edge:
			self.update_list.append((col - 1, row + 1))
		# bottom
		if not bottom_edge:
			self.update_list.append((col, row + 1))
		# bottom-right
		if (not bottom_edge and not right_edge):
			self.update_list.append((col + 1, row + 1))

	def create_neighbor_count_list(self):
		self.neighbor_count_list = []
		for cell in self.update_list:
			neighbors = self.get_neighbor_count_list(cell[0], cell[1])
			self.neighbor_count_list.append((cell[0], cell[1], neighbors))

	def get_neighbor_count_list(self, col, row):
		top_edge = row == 0
		bottom_edge = row == self.size[1] - 1
		left_edge = col == 0
		right_edge = col == self.size[0] - 1

		neighbors = 0

		# top-left
		if not top_edge and not left_edge:
			neighbors += self.cell_inside_cells_list(col - 1, row - 1)
		# top
		if not top_edge:
			neighbors += self.cell_inside_cells_list(col, row - 1)
		# top-right
		if not top_edge and not right_edge:
			neighbors += self.cell_inside_cells_list(col + 1, row - 1)
		# left
		if not left_edge:
			neighbors += self.cell_inside_cells_list(col - 1, row)
		# right
		if not right_edge:
			neighbors += self.cell_inside_cells_list(col + 1, row)
		# bottom-left
		if not bottom_edge and not left_edge:
			neighbors += self.cell_inside_cells_list(col - 1, row + 1)
		# bottom
		if not bottom_edge:
			neighbors += self.cell_inside_cells_list(col, row + 1)
		# bottom-right
		if not bottom_edge and not right_edge:
			neighbors += self.cell_inside_cells_list(col + 1, row + 1)

		return neighbors

	def cell_inside_cells_list(self, col, row):
		if (col, row) in self.cells_list:
			return True
		return False

	def change_cells_list_states(self):
		for cell in self.neighbor_count_list:
			neighbors = cell[2]
			if neighbors == 3:
				if not self.cell_inside_cells_list(cell[0], cell[1]):
					self.cells_list.append((cell[0], cell[1]))
			elif neighbors != 2:
				try:
					self.cells_list.remove((cell[0], cell[1]))
				except:
					continue

	def draw_cells(self):
		for cell in self.cells_list:
			color = (255, 255, 255)
			x = self.artist.offset[0] + cell[0] * self.cell_size
			y = self.artist.offset[1] + cell[1] * self.cell_size
			width = self.cell_size
			height = self.cell_size
			thickness = 0

			self.artist.rect(color, x, y, width, height, thickness)

	def draw_neighbor_count_list(self):
		for cell in self.neighbor_count_list:
			x = self.artist.offset[0] + cell[0] * self.cell_size + 0.5 * self.cell_size
			y = self.artist.offset[1] + cell[1] * self.cell_size + 0.5 * self.cell_size
			neighbors = cell[2]
			text = str(neighbors)
			color = self.neighbor_count_color

			self.artist.text(x, y, text, color, "neighbor")

	def draw_updated_cells(self):
		for cell in self.update_list:
			color = (255, 0, 0)
			x = self.artist.offset[0] + cell[0] * self.cell_size
			y = self.artist.offset[1] + cell[1] * self.cell_size
			width = self.cell_size
			height = self.cell_size
			thickness = 0

			self.artist.rect(color, x, y, width, height, thickness)
