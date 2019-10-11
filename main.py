"""
Game of Python - Game of Life implementation written in Python by MyNameIsTrez.

Controls:
    escape - exits the program
    f - fullscreen_bool
    d - draw the debug info
    n - draw the neighbor counts

You can temporarily get rid of most of the false alerts in your IDE
by adding this in your settings.json file, inside of the curly brackets:
    "python.linting.pylintArgs": [
        "--extension-pkg-whitelist=pygame"  // The extension is "lxml" not "1xml"
    ]

This is the order of the functions this program uses to calculate the cells_list' next state:
    # setup
        grid.set_starter_cells_list() # sets some of the cells_list to True, according to r_pentomino/glider

    # main while loop
        # this next line is unnecessary, just only save the updated cells_list in an empty array
        # (re)makes an empty 1D array for storing the cells_list that are alive, and their neighbors
        grid.create_update_list()
        grid.set_update_list() # sets alive cells_list and their (dead) neighbors to True in update_list

        # this next function seems unnecessary in tests, but it makes sense to call it every frame
        # (re)makes an empty 1D array for storing the cells_list that have a neighbor count
        grid.create_neighbor_count_list()
        grid.set_neighbor_count_list() # uses update_list to update the neighbor count array

        grid.change_cells_list_states() # uses update_list to change the cell array

        # drawing alive cells
"""

# import os
import sys
# import ctypes
# user32 = ctypes.windll.user32
# user32.SetProcessDPIAware()

import time
import math

import pygame.freetype
import pygame

from grid import Grid


def setup():
    """placeholder"""
    # CUSTOM VALUES
    update_interval = 0
    starter_cells_blueprint = 1  # 1 = r_pentomino, 2 = glider
    fullscreen_bool = True
    draw_debug_info_bool = True
    draw_cells_bool = True
    draw_updated_cells_bool = False
    draw_neighbor_count_list_bool = False
    font_type = "arial"
    debug_font_size = 30

    cols = 50
    rows = 50
    cell_size = 20

    # INITIALIZATION
    pygame.init()

    info_object = pygame.display.Info()
    display_w = info_object.current_w
    display_h = info_object.current_h
    size = (cols * cell_size, rows * cell_size)

    grid_offset_x = (display_w - size[0]) / 2
    grid_offset_y = (display_h - size[1]) / 2

    screen = pygame.display.set_mode(
        (0, 0), pygame.FULLSCREEN if fullscreen_bool else 0)
    font_debug = pygame.freetype.SysFont(font_type, debug_font_size)
    font_neighbor = pygame.freetype.SysFont(font_type, cell_size)
    grid = Grid(cols, rows, cell_size, font_neighbor,
                starter_cells_blueprint, grid_offset_x, grid_offset_y, screen)

    grid.set_starter_cells_list()

    fill_screen(screen, grid.offset_x, grid.offset_y, size)

    grid.create_update_list()
    grid.create_neighbor_count_list()

    if draw_cells_bool:
        grid.draw_cells()

    if draw_updated_cells_bool:
        grid.draw_updated_cells()

    return (screen, grid, update_interval, draw_debug_info_bool, draw_neighbor_count_list_bool,
            size, font_debug, cols, rows, draw_cells_bool, draw_updated_cells_bool, display_w, display_h)


def main():
    """placeholder"""
    first_start_time = time.time()

    (screen, grid, update_interval, draw_debug_info_bool, draw_neighbor_count_list_bool,
     size, font_debug, cols, rows, draw_cells_bool, draw_updated_cells_bool, display_w, display_h) = setup()

    draw_debug(draw_debug_info_bool, draw_neighbor_count_list_bool, first_start_time, update_interval,
               size, cols, rows, grid, font_debug, draw_cells_bool, draw_updated_cells_bool, display_w, display_h, screen)

    pygame.display.flip()  # draw this frame

    sleep(update_interval, first_start_time)

    running_bool = True
    while running_bool:
        start_time = time.time()

        running_bool, draw_debug_info_bool, draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool = get_inputs(
            screen, size, running_bool, draw_debug_info_bool,
            draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool)

        fill_screen(screen, grid.offset_x, grid.offset_y, size)

        grid.create_update_list()

        # this next function seems unnecessary in tests, but it makes sense to call it every frame
        grid.create_neighbor_count_list()

        grid.change_cells_list_states()

        if draw_cells_bool:
            grid.draw_cells()
        if draw_updated_cells_bool:
            grid.draw_updated_cells()

        draw_debug(draw_debug_info_bool, draw_neighbor_count_list_bool, start_time, update_interval,
                   size, cols, rows, grid, font_debug, draw_cells_bool, draw_updated_cells_bool, display_w, display_h, screen)

        pygame.display.flip()  # draw this frame

        sleep(update_interval, start_time)


def fill_screen(screen, offset_x, offset_y, size):
    """placeholder"""
    screen.fill((25, 25, 25))  # make the entire screen dark gray
    # draw a rectangle to fill the area of the grid
    pygame.draw.rect(
        screen, (50, 50, 50),  # gray
        (offset_x, offset_y, size[0], size[1]),  # x, y, width, height
        0  # thickness, 0 means fill instead
    )


def draw_debug(draw_debug_info_bool, draw_neighbor_count_list_bool, start_time, update_interval,
               size, cols, rows, grid, font_debug, draw_cells_bool, draw_updated_cells_bool, display_w, display_h, screen):
    """drawing stats that can help when debugging"""
    if draw_neighbor_count_list_bool:
        grid.draw_neighbor_count_list()

    if draw_debug_info_bool:
        text = []

        partial_time_elapsed = time.time() - start_time

        # ms taken from max ms
        string = str(math.floor(partial_time_elapsed * 1000))
        if update_interval != 0:
            string += "/" + str(math.floor(update_interval * 1000)) + " ms"
        else:
            string += " ms"
        string += " to calculate this frame"
        text.append(string)

        # potential_speed_multiplier
        if partial_time_elapsed > 0:
            potential_speed_multiplier = round(
                update_interval / partial_time_elapsed, 1)
        else:
            potential_speed_multiplier = "?"

        if update_interval != 0:
            text.append("the program can run at " +
                        str(potential_speed_multiplier) + "x the current speed")
        else:
            text.append("the program is running as fast as it can!")

        text.append("grid size: " + str(cols) + "x" + str(rows))
        text.append("program resolution: " + str(size[0]) + "x" + str(size[1]))
        text.append("display resolution: " +
                    str(display_w) + "x" + str(display_h))
        text.append("draw cells: " + str(draw_cells_bool))
        text.append("draw updated cells: " + str(draw_updated_cells_bool))
        text.append("draw neighbor count: " +
                    str(draw_neighbor_count_list_bool))
        text.append("cells alive: " + str(len(grid.cells_list)))
        text.append("cells updated: " + str(len(grid.update_list)))
        text.append("cell neighbors: " + str(len(grid.neighbor_count_list)))

        for i, val in enumerate(text):
            pos = (25, 25 + 40 * i)
            font_debug.render_to(screen, pos, val, (150, 150, 255))


def sleep(update_interval, start_time):
    """placeholder"""
    final_time_elapsed = time.time() - start_time
    sleep_time = max(update_interval - final_time_elapsed, 0)
    time.sleep(sleep_time)


def get_inputs(screen, size, running_bool, draw_debug_info_bool,
               draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool):
    """placeholder"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # needed to register multiple keys being held down at once
            keys = pygame.key.get_pressed()
            # exit the program
            if keys[pygame.K_ESCAPE]:
                running_bool = False  # sets running_bool to False to exit the while loop
            # toggle fullscreen_bool
            if keys[pygame.K_f]:
                if screen.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode((0, 0))
                else:
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
    return running_bool, draw_debug_info_bool, draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool


main()
