"""
Game of Python - Game of Life implementation written in Python by MyNameIsTrez.

Controls:
	escape - exits the program
	f - go to fullscreen/windowed mode
	1, 2, 3, 4 on the keyboard - toggles what is drawn

Rules of Game of Life:
	- Each white rectangle on the screen is called an 'alive cell',
	  the surrounding light gray rectangles area consists of 'dead cells'.
	- Each cell has 8 neighbors next to it.
	- If a cell has 3 alive neighbors, it also becomes alive/stays alive.
	- If a cell has 2 alive neighbors, it stays alive.
	- If a cell has any other number of neighbors, it dies of under-/overpopulation.

You can temporarily get rid of most of the pylint alerts in the Visual Studio Code editor
by adding this in your settings.json file, inside of the curly brackets:
	"python.linting.pylintArgs": [
		"--extension-pkg-whitelist=pygame"  // The extension is "lxml" not "1xml"
	]
"""

import time
import math

import pygame.freetype
import pygame

from grid import Grid
from graph import Graph
from artist import Artist

# from multiprocessing import Pool


def setup():
	# CUSTOM VALUES
	cols = 50
	rows = 50
	cell_size = 10

	update_interval = 0.1
	starter_cells_blueprint = 1  # 1 = r_pentomino, 2 = glider
	random_starter_cells = False  # WARNING: VERY LAGGY
	fullscreen_bool = True
	draw_debug_info_bool = True
	draw_cells_bool = True
	draw_updated_cells_bool = False
	draw_neighbor_count_list_bool = False
	font_type = "arial"

	# INITIALIZATION
	pygame.init()

	info_object = pygame.display.Info()
	display_w = info_object.current_w
	display_h = info_object.current_h
	size = (width, height) = (cols * cell_size, rows * cell_size)

	if fullscreen_bool:
		pygame.display.set_mode((display_w, display_h))
	screen = pygame.display.set_mode((0, 0) if fullscreen_bool else size,
                                  pygame.FULLSCREEN if fullscreen_bool else 0)
	debug_font_size = cell_size * 3
	font_debug = pygame.freetype.SysFont(font_type, debug_font_size)

	artist = Artist(screen, width, height)
	artist.offset_fullscreen = (
            (display_w - size[0]) / 2, (display_h - size[1]) / 2)
	artist.offset = artist.offset_fullscreen if fullscreen_bool else 0

	font_neighbor = pygame.freetype.SysFont(font_type, cell_size)
	grid = Grid(cols, rows, cell_size, font_neighbor,
             starter_cells_blueprint, random_starter_cells, artist, screen)

	grid.offset_fullscreen = (
		(display_w - size[0]) / 2, (display_h - size[1]) / 2)
	grid.offset = grid.offset_fullscreen if fullscreen_bool else 0

	grid.set_starter_cells_list()

	grid.create_update_list()
	grid.create_neighbor_count_list()

	fill_screen(screen, grid.offset, size)

	if draw_cells_bool:
		grid.draw_cells()

	if draw_updated_cells_bool:
		grid.draw_updated_cells()

	graph = Graph(screen, width, height, artist)
	graph.offset_fullscreen = (
		(display_w - size[0]) / 2, (display_h - size[1]) / 2)
	graph.offset = graph.offset_fullscreen if fullscreen_bool else 0

	return (screen, grid, update_interval, draw_debug_info_bool, draw_neighbor_count_list_bool,
         size, font_debug, draw_cells_bool, draw_updated_cells_bool, display_w, display_h, graph)


def main():
	first_start_time = time.time()

	(screen, grid, update_interval, draw_debug_info_bool,
	 draw_neighbor_count_list_bool, size, font_debug,
	 draw_cells_bool, draw_updated_cells_bool, display_w, display_h, graph) = setup()

	draw_debug(draw_debug_info_bool, draw_neighbor_count_list_bool,
            first_start_time, update_interval, size, grid, font_debug,
            draw_cells_bool, draw_updated_cells_bool, display_w, display_h, graph, screen)

	pygame.display.flip()  # draw this frame

	sleep(update_interval, first_start_time)

	running_bool = True
	state = "simulating"
	while running_bool:
		(
			running_bool, draw_debug_info_bool, draw_cells_bool,
			draw_updated_cells_bool, draw_neighbor_count_list_bool, state
		) = get_inputs(
			screen, size, display_w, display_h, grid, running_bool, draw_debug_info_bool,
			draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool, state, graph
		)

		if state == "simulating":
			start_time = time.time()

			fill_screen(screen, grid.offset, size)

			grid.create_update_list()

			# this next function seems unnecessary in tests, but it makes sense to call it every frame
			grid.create_neighbor_count_list()

			grid.change_cells_list_states()

			if draw_cells_bool:
				grid.draw_cells()
			if draw_updated_cells_bool:
				grid.draw_updated_cells()

			draw_debug(draw_debug_info_bool, draw_neighbor_count_list_bool, start_time, update_interval,
                            size, grid, font_debug, draw_cells_bool, draw_updated_cells_bool, display_w, display_h, graph, screen)

			pygame.display.flip()  # draw this frame

			sleep(update_interval, start_time)
		elif state == "showing graph":
			graph.draw()
			pygame.display.flip()  # draw this frame


def fill_screen(screen, offset, size):
	screen.fill((25, 25, 25))  # make the entire screen dark gray
	# draw a rectangle to fill the area of the grid
	pygame.draw.rect(
		screen, (50, 50, 50),  # gray
		(offset[0], offset[1], size[0], size[1]),  # x, y, width, height
		0  # thickness, 0 means fill instead
	)


def draw_debug(draw_debug_info_bool, draw_neighbor_count_list_bool, start_time, update_interval,
               size, grid, font_debug, draw_cells_bool, draw_updated_cells_bool, display_w, display_h, graph, screen):
	# drawing stats that can help when debugging
	if draw_neighbor_count_list_bool:
		grid.draw_neighbor_count_list()

	if draw_debug_info_bool:
		data = {}
		text = []

		partial_time_elapsed = time.time() - start_time
		ms = math.ceil(partial_time_elapsed * 1000)
		data["ms/frame"] = ms
		ms_interval = math.ceil(update_interval * 1000)

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
		if update_interval != 0:
			string += "/" + str(ms_interval)
		string += " ms/frame"
		text.append(string)

		# ms/cell alive
		ms_per_cell_alive = round(ms / len(grid.cells_list), 2)
		string = str(ms_per_cell_alive) + " ms/cell alive"
		text.append(string)
		data["ms/cell alive"] = ms_per_cell_alive

		# ms/cell updated
		ms_per_cell_updated = round(ms / len(grid.update_list), 2)
		string = str(ms_per_cell_updated) + " ms/cell updated"
		text.append(string)
		data["ms/cell updated"] = ms_per_cell_updated

		# potential_speed_multiplier
		if partial_time_elapsed > 0 and update_interval != 0:
			potential_speed_multiplier = round(
				update_interval / partial_time_elapsed, 1)
		else:
			potential_speed_multiplier = None

		if update_interval != 0:
			text.append("the program can run at " +
                            str(potential_speed_multiplier) + "x the current speed")
		else:
			text.append("the program is running as fast as it can")
		data["potential speed multiplier"] = potential_speed_multiplier

		text.append("grid size: " +
                    str(grid.size[0]) + "x" + str(grid.size[1]))
		text.append("total cell count: " + str(grid.total_cell_count))

		cells_dead = grid.total_cell_count - len(grid.cells_list)
		text.append("cells dead: " + str(cells_dead))
		data["cells dead"] = cells_dead

		cells_alive = len(grid.cells_list)
		text.append("cells alive: " + str(cells_alive))
		data["cells alive"] = cells_alive

		cells_updated = len(grid.update_list)
		text.append("cells updated: " + str(cells_updated))
		data["cells updated"] = cells_updated

		text.append("draw cells: " + str(draw_cells_bool))
		text.append("draw updated cells: " + str(draw_updated_cells_bool))
		text.append("draw neighbor count: " +
                    str(draw_neighbor_count_list_bool))

		text.append("cell size: " + str(grid.cell_size))
		text.append("program resolution: " + str(size[0]) + "x" + str(size[1]))
		text.append("display resolution: " +
                    str(display_w) + "x" + str(display_h))

		for i, val in enumerate(text):
			pos = (2 * grid.cell_size, 2 * grid.cell_size + 4 * grid.cell_size * i)
			font_debug.render_to(screen, pos, val, (150, 150, 255))

		graph.data.append(data)


def sleep(update_interval, start_time):
	final_time_elapsed = time.time() - start_time
	sleep_time = max(update_interval - final_time_elapsed, 0)
	time.sleep(sleep_time)


def get_inputs(screen, size, display_w, display_h, grid, running_bool, draw_debug_info_bool,
               draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool, state, graph):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running_bool = False  # sets running_bool to False to exit the while loop
		elif event.type == pygame.KEYDOWN:
			# needed to register multiple keys being held down at once
			keys = pygame.key.get_pressed()

			# exit the program
			if keys[pygame.K_ESCAPE]:
				running_bool = False  # sets running_bool to False to exit the while loop

			# toggle fullscreen_bool
			if keys[pygame.K_f]:
				if screen.get_flags() & pygame.FULLSCREEN:
					grid.offset = (0, 0)
					graph.offset = (0, 0)

					pygame.display.set_mode(size)
				else:
					grid.offset = grid.offset_fullscreen
					graph.offset = graph.offset_fullscreen

					# we first resize the window to the size it'd be in fullscreen, then we fullscreen
					pygame.display.set_mode((display_w, display_h))
					pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

			# what debug info to draw
			if keys[pygame.K_1]:
				draw_debug_info_bool = not draw_debug_info_bool
			if keys[pygame.K_2]:
				draw_cells_bool = not draw_cells_bool
			if keys[pygame.K_3]:
				draw_updated_cells_bool = not draw_updated_cells_bool
			if keys[pygame.K_4]:
				draw_neighbor_count_list_bool = not draw_neighbor_count_list_bool
			if keys[pygame.K_5]:
				if state == "simulating":
					state = "showing graph"
				elif state == "showing graph":
					state = "simulating"

	return running_bool, draw_debug_info_bool, draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool, state


if __name__ == '__main__':
	main()
