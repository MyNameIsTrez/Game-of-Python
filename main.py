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

You can temporarily get rid of most of the pylint alerts in the IDE
by adding this in your settings.json file, inside of the curly brackets:
    "python.linting.pylintArgs": [
        "--extension-pkg-whitelist=pygame"  // The extension is "lxml" not "1xml"
    ]
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
    cols = 100
    rows = 100
    cell_size = 10

    update_interval = 0
    starter_cells_blueprint = 1  # 1 = r_pentomino, 2 = glider
    random_starter_cells = False  # WARNING: VERY LAGGY
    fullscreen_bool = False
    draw_debug_info_bool = True
    draw_cells_bool = True
    draw_updated_cells_bool = False
    draw_neighbor_count_list_bool = False
    font_type = "arial"
    debug_font_size = 30

    # INITIALIZATION
    pygame.init()

    info_object = pygame.display.Info()
    display_w = info_object.current_w
    display_h = info_object.current_h
    size = (cols * cell_size, rows * cell_size)

    if fullscreen_bool:
        pygame.display.set_mode((display_w, display_h))
    screen = pygame.display.set_mode(
        (0, 0) if fullscreen_bool else size, pygame.FULLSCREEN if fullscreen_bool else 0)
    font_debug = pygame.freetype.SysFont(font_type, debug_font_size)

    font_neighbor = pygame.freetype.SysFont(font_type, cell_size)
    grid = Grid(cols, rows, cell_size, font_neighbor,
                starter_cells_blueprint, random_starter_cells, screen)

    grid.offset_x_fullscreen = (display_w - size[0]) / 2
    grid.offset_y_fullscreen = (display_h - size[1]) / 2
    grid.offset_x = grid.offset_x_fullscreen if fullscreen_bool else 0
    grid.offset_y = grid.offset_y_fullscreen if fullscreen_bool else 0

    grid.set_starter_cells_list()

    grid.create_update_list()
    grid.create_neighbor_count_list()

    fill_screen(screen, grid.offset_x, grid.offset_y, size)

    if draw_cells_bool:
        grid.draw_cells()

    if draw_updated_cells_bool:
        grid.draw_updated_cells()

    return (screen, grid, update_interval, draw_debug_info_bool, draw_neighbor_count_list_bool,
            size, font_debug, draw_cells_bool, draw_updated_cells_bool, display_w, display_h)


def main():
    """placeholder"""
    first_start_time = time.time()

    (screen, grid, update_interval, draw_debug_info_bool,
     draw_neighbor_count_list_bool, size, font_debug,
     draw_cells_bool, draw_updated_cells_bool, display_w, display_h) = setup()

    draw_debug(draw_debug_info_bool, draw_neighbor_count_list_bool,
               first_start_time, update_interval, size, grid, font_debug,
               draw_cells_bool, draw_updated_cells_bool, display_w, display_h, screen)

    pygame.display.flip()  # draw this frame

    sleep(update_interval, first_start_time)

    running_bool = True
    while running_bool:
        start_time = time.time()

        (running_bool, draw_debug_info_bool, draw_cells_bool,
         draw_updated_cells_bool, draw_neighbor_count_list_bool) = get_inputs(
             screen, size, display_w, display_h, grid, running_bool, draw_debug_info_bool,
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
                   size, grid, font_debug, draw_cells_bool, draw_updated_cells_bool, display_w, display_h, screen)

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
               size, grid, font_debug, draw_cells_bool, draw_updated_cells_bool, display_w, display_h, screen):
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
            text.append("the program is running as fast as it can")

        text.append("grid size: " +
                    str(grid.size[0]) + "x" + str(grid.size[1]))
        text.append("total cell count: " + str(grid.total_cell_count))

        text.append("cells dead: " +
                    str(grid.total_cell_count - len(grid.cells_list)))
        text.append("cells alive: " + str(len(grid.cells_list)))
        text.append("cells updated: " + str(len(grid.update_list)))
        text.append("cell neighbors: " + str(len(grid.neighbor_count_list)))

        text.append("draw cells: " + str(draw_cells_bool))
        text.append("draw updated cells: " + str(draw_updated_cells_bool))
        text.append("draw neighbor count: " +
                    str(draw_neighbor_count_list_bool))

        text.append("cell size: " + str(grid.cell_size))
        text.append("program resolution: " + str(size[0]) + "x" + str(size[1]))
        text.append("display resolution: " +
                    str(display_w) + "x" + str(display_h))

        for i, val in enumerate(text):
            pos = (25, 25 + 40 * i)
            font_debug.render_to(screen, pos, val, (150, 150, 255))


def sleep(update_interval, start_time):
    """placeholder"""
    final_time_elapsed = time.time() - start_time
    sleep_time = max(update_interval - final_time_elapsed, 0)
    time.sleep(sleep_time)


def get_inputs(screen, size, display_w, display_h, grid, running_bool, draw_debug_info_bool,
               draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool):
    """placeholder"""
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
                    grid.offset_x = 0
                    grid.offset_y = 0
                    pygame.display.set_mode(size)
                else:
                    grid.offset_x = grid.offset_x_fullscreen
                    grid.offset_y = grid.offset_y_fullscreen
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
    return running_bool, draw_debug_info_bool, draw_cells_bool, draw_updated_cells_bool, draw_neighbor_count_list_bool


main()
