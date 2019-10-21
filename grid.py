
import math
import random
import time

# from multiprocessing import Pool
# from functools import partial

import pygame


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

	def __init__(self, cols, rows, cell_size, font_neighbor,
              starter_cells_blueprint, random_starter_cells, screen):
		self.size = (cols, rows)
		self.cell_size = cell_size
		self.font_neighbor = font_neighbor
		self.screen = screen
		# makes a 1D array for storing the cols and rows of cells that are alive
		self.cells_list = []
		self.neighbor_count_list = None
		self.update_list = None
		self.starter_cells_blueprint = starter_cells_blueprint
		self.offset_x = 0
		self.offset_y = 0
		self.total_cell_count = cols * rows
		self.random_starter_cells = random_starter_cells
		# self.pool = Pool()

	def set_starter_cells_list(self):
		# adds some cells to cells_list, according to the r_pentomino/glider blueprints
		o_x = math.floor(self.size[0] / 2)  # offset_x
		o_y = math.floor(self.size[1] / 2)  # offset_y

		if self.random_starter_cells:
			for col in range(self.size[0]):
				for row in range(self.size[1]):
					if random.randint(0, 1):
						self.cells_list.append((col, row))
		else:
			if self.starter_cells_blueprint == 1:
				# r_pentomino
				self.cells_list.append((0 + o_x, 1 + o_y))
				self.cells_list.append((1 + o_x, 0 + o_y))
				self.cells_list.append((1 + o_x, 1 + o_y))
				self.cells_list.append((1 + o_x, 2 + o_y))
				self.cells_list.append((2 + o_x, 0 + o_y))
			else:
				# glider
				# useful for checking if the cell states are being set incorrectly
				self.cells_list.append((0 + o_x, 1 + o_y))
				self.cells_list.append((1 + o_x, 2 + o_y))
				self.cells_list.append((2 + o_x, 2 + o_y))
				self.cells_list.append((2 + o_x, 1 + o_y))
				self.cells_list.append((2 + o_x, 0 + o_y))

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
			pygame.draw.rect(
				self.screen, (255, 255, 255),  # white
				(self.offset_x + cell[0] * self.cell_size,  # x
				 self.offset_y + cell[1] * self.cell_size,  # y
				 self.cell_size, self.cell_size),  # width, height
				0  # thickness, 0 means fill instead
			)

	def draw_neighbor_count_list(self):
		for cell in self.neighbor_count_list:
			neighbors = cell[2]

			coords = (self.offset_x + cell[0] * self.cell_size + 0.5 * self.cell_size,
                            self.offset_y + cell[1] * self.cell_size + 0.5 * self.cell_size)
			self.font_neighbor.render_to(
				self.screen, coords, str(neighbors), (255, 50, 50))

	def draw_updated_cells(self):
		for cell in self.update_list:
			pygame.draw.rect(
				self.screen, (255, 0, 0),  # red
				(self.offset_x + cell[0] * self.cell_size,  # x
				 self.offset_y + cell[1] * self.cell_size,  # y
				 self.cell_size, self.cell_size),  # width, height
				0  # thickness, 0 means fill instead
			)
