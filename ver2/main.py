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

This is the order of the functions this program uses to calculate the cells' next state:
    # setup
        grid.create_cells() # makes a 2D array called cells, and fills it with Falses
        grid.set_starter_cells() # sets some of the cells to True, according to r_pentomino/glider

    # main while loop
        grid.create_update_list() # remakes a 2D array called update_list, and fills it with Falses
        grid.set_update_list() # sets alive cells and their (dead) neighbors to True in update_list

        # this next function seems unnecessary in tests, but it makes sense to call it every frame
        grid.create_neighbor_count() # (re)makes a 2D array with a neighbor count of 0 for each cell
        grid.set_neighbor_count() # uses update_list to update the neighbor count array

        grid.set_cells_state() # uses update_list to change the cell array

        # drawing alive cells
"""

import sys
import time
import math

import pygame.freetype
import pygame

from grid import Grid


def setup():
    """placeholder"""
    # CUSTOM VALUES
    fullscreen_bool = False
    update_interval = 0
    draw_debug_info_bool = True
    draw_neighbor_count_bool = False
    font_type = "arial"
    debug_font_size = 30
    draw_cells_bool = True
    starter_cells_blueprint = 1  # 1 = r_pentomino, 2 = glider

    cols = 50
    rows = 50
    cell_size = 20

    # INITIALIZATION
    pygame.init()

    neighbor_font_size = cell_size
    info_object = pygame.display.Info()
    screen_width, screen_height = info_object.current_w, info_object.current_h
    size = (min(cols * cell_size, screen_width),
            min(rows * cell_size, screen_height))

    screen = pygame.display.set_mode(
        size, pygame.FULLSCREEN if fullscreen_bool else 0)
    font_debug = pygame.freetype.SysFont(font_type, debug_font_size)
    font_neighbor = pygame.freetype.SysFont(font_type, neighbor_font_size)
    grid = Grid(cols, rows, cell_size, font_neighbor,
                starter_cells_blueprint, screen)  # create the grid

    grid.create_cells()
    grid.set_starter_cells()

    return (screen, grid, update_interval, draw_debug_info_bool,
            draw_neighbor_count_bool, size, font_debug, cols, rows, draw_cells_bool)


def main():
    """placeholder"""
    first_start_time = time.time()

    (screen, grid, update_interval, draw_debug_info_bool, draw_neighbor_count_bool,
     size, font_debug, cols, rows, draw_cells_bool) = setup()

    fill_screen(screen)

    if draw_cells_bool:
        grid.draw_cells()

    # grid.draw_updated_cells()

    draw_debug(draw_debug_info_bool, draw_neighbor_count_bool, first_start_time,
               update_interval, size, cols, rows, grid, font_debug, draw_cells_bool, screen)

    pygame.display.flip()
    time.sleep(update_interval)

    running_bool = True
    while running_bool:
        start_time = time.time()

        running_bool, draw_debug_info_bool, draw_cells_bool, draw_neighbor_count_bool = get_inputs(
            screen, size, running_bool, draw_debug_info_bool,
            draw_cells_bool, draw_neighbor_count_bool)

        fill_screen(screen)

        grid.create_update_list()
        grid.set_update_list()

        # this next function seems unnecessary in tests, but it makes sense to call it every frame
        grid.create_neighbor_count()
        grid.set_neighbor_count()

        grid.set_cells_state()

        if draw_cells_bool:
            grid.draw_cells()

        # grid.draw_updated_cells()

        draw_debug(draw_debug_info_bool, draw_neighbor_count_bool, start_time, update_interval,
                   size, cols, rows, grid, font_debug, draw_cells_bool, screen)

        pygame.display.flip()  # draw this frame

        sleep(update_interval, start_time)


def fill_screen(screen):
    """placeholder"""
    screen.fill((50, 50, 50))  # make the screen gray


def get_inputs(screen, size, running_bool, draw_debug_info_bool,
               draw_cells_bool, draw_neighbor_count_bool):
    """placeholder"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # needed to register multiple keys being held down at once
            keys = pygame.key.get_pressed()
            # exit the program
            if event.key == pygame.K_ESCAPE:
                running_bool = False  # sets running_bool to False to exit the while loop
            # toggle fullscreen_bool
            if event.key == pygame.K_f:
                if screen.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode(size)
                else:
                    pygame.display.set_mode(size, pygame.FULLSCREEN)
            # what debug info to draw
            if keys[pygame.K_d]:
                if keys[pygame.K_1]:
                    draw_debug_info_bool = not draw_debug_info_bool
                if keys[pygame.K_2]:
                    draw_cells_bool = not draw_cells_bool
                if keys[pygame.K_3]:
                    draw_neighbor_count_bool = not draw_neighbor_count_bool
    return running_bool, draw_debug_info_bool, draw_cells_bool, draw_neighbor_count_bool


def draw_debug(draw_debug_info_bool, draw_neighbor_count_bool, start_time, update_interval,
               size, cols, rows, grid, font_debug, draw_cells_bool, screen):
    """code that has to do with drawing stats that can help with debugging"""
    if draw_neighbor_count_bool:
        grid.draw_neighbor_count_bool()

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
        potential_speed_multiplier = round(
            update_interval / partial_time_elapsed, 1)
        if update_interval != 0:
            text.append("the program can run at " +
                        str(potential_speed_multiplier) + "x the current speed")
        else:
            text.append("the program is running as fast as it can!")

        # grid size
        text.append("grid size: " + str(cols) + "x" + str(rows))

        # resolution
        text.append("resolution: " + str(size[0]) + "x" + str(size[1]))

        # whether the cells are being drawn on the screen
        text.append("draw cells: " + str(draw_cells_bool))

        # whether the neighor count is being drawn, necessary to display it for when it's unreadable
        text.append("draw neighbor count: " + str(draw_neighbor_count_bool))

        for i, val in enumerate(text):
            pos = (25, 25 + 40 * i)
            font_debug.render_to(screen, pos, val, (150, 150, 255))


def sleep(update_interval, start_time):
    """placeholder"""
    final_time_elapsed = time.time() - start_time
    sleep_time = max(update_interval - final_time_elapsed, 0)
    time.sleep(sleep_time)


main()
