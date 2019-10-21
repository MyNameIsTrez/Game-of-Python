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
from debug_info import Debug_Info

# from multiprocessing import Pool


def setup():
	# CUSTOM VALUES
	cols = 50
	rows = 50
	cell_size = 10

	update_interval = 0.1
	starter_cells_blueprint = 1  # 1 = r_pentomino, 2 = glider
	random_starter_cells = False  # WARNING: VERY LAGGY
	fullscreen_bool = False
	draw_debug_info_bool = True
	draw_cells_bool = True
	draw_updated_cells_bool = False
	draw_neighbor_count_list_bool = False
	font_type = "arial"
	neighbor_count_color = (255, 0, 0)

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
	font_neighbor = pygame.freetype.SysFont(font_type, cell_size)
	artist = Artist(screen, width, height, font_neighbor, font_debug)

	artist.offset_fullscreen = (
            (display_w - size[0]) / 2, (display_h - size[1]) / 2)
	artist.offset = artist.offset_fullscreen if fullscreen_bool else (0, 0)

	grid = Grid(cols, rows, cell_size, neighbor_count_color,
             starter_cells_blueprint, random_starter_cells, artist, screen)

	grid.set_starter_cells_list()

	grid.create_update_list()
	grid.create_neighbor_count_list()

	artist.fill_screen()

	if draw_cells_bool:
		grid.draw_cells()

	if draw_updated_cells_bool:
		grid.draw_updated_cells()

	graph = Graph(screen, width, height, artist)
	debug_info = Debug_Info(
		draw_debug_info_bool, draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool,
		grid, update_interval, size, display_w, display_h, artist, graph
	)

	return (screen, grid, update_interval, draw_debug_info_bool, draw_neighbor_count_list_bool,
         size, draw_cells_bool, draw_updated_cells_bool, display_w, display_h, graph, artist, debug_info)


def main():
	first_start_time = time.time()

	(screen, grid, update_interval, draw_debug_info_bool,
	 draw_neighbor_count_list_bool, size, draw_cells_bool,
	 draw_updated_cells_bool, display_w, display_h, graph, artist, debug_info) = setup()

	debug_info.draw(first_start_time)

	pygame.display.flip()  # draw this frame

	sleep(update_interval, first_start_time)

	debug_info.state = "simulating"
	while debug_info.running_bool:
		get_inputs(screen, size, display_w, display_h,
		           grid, graph, artist, debug_info)

		if debug_info.state == "simulating":
			start_time = time.time()

			artist.fill_screen()

			grid.create_update_list()

			# this next function seems unnecessary in tests, but it makes sense to call it every frame
			grid.create_neighbor_count_list()

			grid.change_cells_list_states()

			if debug_info.draw_cells_bool:
				grid.draw_cells()
			if debug_info.draw_updated_cells_bool:
				grid.draw_updated_cells()

			debug_info.draw(start_time)

			pygame.display.flip()  # draw this frame

			sleep(update_interval, start_time)
		elif debug_info.state == "showing graph":
			graph.draw()
			pygame.display.flip()  # draw this frame


def sleep(update_interval, start_time):
	final_time_elapsed = time.time() - start_time
	sleep_time = max(update_interval - final_time_elapsed, 0)
	time.sleep(sleep_time)


def get_inputs(screen, size, display_w, display_h, grid, graph, artist, debug_info):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			debug_info.running_bool = False  # sets running_bool to False to exit the while loop
		elif event.type == pygame.KEYDOWN:
			# needed to register multiple keys being held down at once
			keys = pygame.key.get_pressed()

			# exit the program
			if keys[pygame.K_ESCAPE]:
				debug_info.running_bool = False  # sets running_bool to False to exit the while loop

			# toggle fullscreen_bool
			if keys[pygame.K_f]:
				if screen.get_flags() & pygame.FULLSCREEN:
					artist.offset = (0, 0)

					pygame.display.set_mode(size)
				else:
					artist.offset = artist.offset_fullscreen

					# we first resize the window to the size it'd be in fullscreen, then we fullscreen
					pygame.display.set_mode((display_w, display_h))
					pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

			# what debug info to draw
			if keys[pygame.K_1]:
				debug_info.draw_debug_info_bool = not debug_info.draw_debug_info_bool
			if keys[pygame.K_2]:
				debug_info.draw_cells_bool = not debug_info.draw_cells_bool
			if keys[pygame.K_3]:
				debug_info.draw_updated_cells_bool = not debug_info.draw_updated_cells_bool
			if keys[pygame.K_4]:
				debug_info.draw_neighbor_count_list_bool = not debug_info.draw_neighbor_count_list_bool
			if keys[pygame.K_5]:
				if debug_info.state == "simulating":
					debug_info.state = "showing graph"
				elif debug_info.state == "showing graph":
					debug_info.state = "simulating"


if __name__ == '__main__':
	main()
