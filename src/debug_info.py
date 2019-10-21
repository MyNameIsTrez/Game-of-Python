import time
import math


class Debug_Info:
	def __init__(self, draw_debug_info_bool, draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool,
              grid, update_interval, size, display_w, display_h, artist, graph):
		self.draw_debug_info_bool = draw_debug_info_bool
		self.draw_cells_bool = draw_cells_bool
		self.draw_updated_cells_bool = draw_updated_cells_bool
		self.draw_neighbor_count_list_bool = draw_neighbor_count_list_bool
		self.grid = grid
		self.update_interval = update_interval
		self.size = size
		self.display_w = display_w
		self.display_h = display_h
		self.artist = artist
		self.graph = graph

		self.running_bool = True
		self.state = "simulating"

	def draw(self, start_time):
		# drawing stats that can help when debugging
		if self.draw_neighbor_count_list_bool:
			self.grid.draw_neighbor_count_list()

		if self.draw_debug_info_bool:
			data = {}
			text = []

			partial_time_elapsed = time.time() - start_time
			ms = math.ceil(partial_time_elapsed * 1000)
			data["ms/frame"] = ms
			ms_interval = math.ceil(self.update_interval * 1000)

			# fps
			if partial_time_elapsed > 0:
				fps = math.ceil(1 / partial_time_elapsed)
			else:
				fps = None

			if (fps):
				string = str(fps) + " fps"
			else:
				string = "None fps"
			text.append(string)
			data["fps"] = fps

			# ms/frame
			string = str(ms)
			if self.update_interval != 0:
				string += "/" + str(ms_interval)
			string += " ms/frame"
			text.append(string)

			# ms/cell alive
			ms_per_cell_alive = round(ms / len(self.grid.cells_list), 2)
			string = str(ms_per_cell_alive) + " ms/cell alive"
			text.append(string)
			data["ms/cell alive"] = ms_per_cell_alive

			# ms/cell updated
			ms_per_cell_updated = round(ms / len(self.grid.update_list), 2)
			string = str(ms_per_cell_updated) + " ms/cell updated"
			text.append(string)
			data["ms/cell updated"] = ms_per_cell_updated

			# potential_speed_multiplier
			if partial_time_elapsed > 0 and self.update_interval != 0:
				potential_speed_multiplier = round(
					self.update_interval / partial_time_elapsed, 1)
			else:
				potential_speed_multiplier = None

			if self.update_interval != 0:
				text.append("the program can run at " +
                                    str(potential_speed_multiplier) + "x the current speed")
			else:
				text.append("the program is running as fast as it can")
			data["potential speed multiplier"] = potential_speed_multiplier

			text.append("grid size: " +
                            str(self.grid.size[0]) + "x" + str(self.grid.size[1]))
			text.append("total cell count: " + str(self.grid.total_cell_count))

			cells_dead = self.grid.total_cell_count - len(self.grid.cells_list)
			text.append("cells dead: " + str(cells_dead))
			data["cells dead"] = cells_dead

			cells_alive = len(self.grid.cells_list)
			text.append("cells alive: " + str(cells_alive))
			data["cells alive"] = cells_alive

			cells_updated = len(self.grid.update_list)
			text.append("cells updated: " + str(cells_updated))
			data["cells updated"] = cells_updated

			text.append("draw cells: " + str(self.draw_cells_bool))
			text.append("draw updated cells: " + str(self.draw_updated_cells_bool))
			text.append("draw neighbor count: " +
                            str(self.draw_neighbor_count_list_bool))

			text.append("cell size: " + str(self.grid.cell_size))
			text.append("program resolution: " +
			            str(self.size[0]) + "x" + str(self.size[1]))
			text.append("display resolution: " +
                            str(self.display_w) + "x" + str(self.display_h))

			for i, text in enumerate(text):
				x = 2 * self.grid.cell_size
				y = 2 * self.grid.cell_size + 4 * self.grid.cell_size * i
				color = (150, 150, 255)
				font = 'debug'
				self.artist.text(x, y, text, color, font)

			self.graph.data.append(data)
