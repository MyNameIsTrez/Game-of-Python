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

import os
import time
import math
import sys

import pygame.freetype
import pygame

from configparser import ConfigParser
from ast import literal_eval

from grid import Grid
from graph import Graph
from artist import Artist
from debug_info import Debug_Info
from event_handler import Event_Handler

# from multiprocessing import Pool


def setup():
	# get the user's config settings from config.ini
	config = ConfigParser()
	config.read(os.path.join(sys.path[0][0:-4], "config.ini"))
	cfg = config["CUSTOM VARIABLES"]

	cols = int(cfg["cols"])
	rows = int(cfg["rows"])
	cell_size = int(cfg["cell_size"])

	update_interval = float(cfg["update_interval"])
	starter_cells_blueprint = int(cfg["starter_cells_blueprint"])
	random_starter_cells = cfg.getboolean("random_starter_cells")
	fullscreen_bool = cfg.getboolean("fullscreen_bool")
	draw_debug_info_bool = cfg.getboolean("draw_debug_info_bool")
	draw_cells_bool = cfg.getboolean("draw_cells_bool")
	draw_updated_cells_bool = cfg.getboolean("draw_updated_cells_bool")
	draw_neighbor_count_list_bool = cfg.getboolean("draw_neighbor_count_list_bool")
	font_type = cfg["font_type"]
	neighbor_count_color = literal_eval(cfg["neighbor_count_color"])
	
	# initialization
	pygame.init()

	info_object = pygame.display.Info()
	display_w = info_object.current_w
	display_h = info_object.current_h
	size = (width, height) = (cols * cell_size, rows * cell_size)

	if fullscreen_bool:
		pygame.display.set_mode((display_w, display_h))

	print(fullscreen_bool)

	screen = pygame.display.set_mode(
		(0, 0) if fullscreen_bool
		else
		size,
		pygame.FULLSCREEN
		if
		fullscreen_bool
		else
		0
	)

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

	event_handler = Event_Handler()

	return (screen, grid, update_interval, draw_debug_info_bool,
         draw_neighbor_count_list_bool, size, draw_cells_bool, draw_updated_cells_bool,
         display_w, display_h, graph, artist, debug_info, event_handler)


def main():
	first_start_time = time.time()

	(screen, grid, update_interval, draw_debug_info_bool,
	 draw_neighbor_count_list_bool, size, draw_cells_bool, draw_updated_cells_bool,
	 display_w, display_h, graph, artist, debug_info, event_handler) = setup()

	debug_info.draw(first_start_time)

	pygame.display.flip()  # draw this frame

	sleep(update_interval, first_start_time)

	debug_info.state = "simulating"
	while debug_info.running_bool:
		event_handler.handle(screen, size, display_w, display_h,
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


if __name__ == '__main__':
	main()
