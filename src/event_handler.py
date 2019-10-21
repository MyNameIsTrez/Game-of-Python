import pygame


class Event_Handler:
	def handle(self, screen, size, display_w, display_h, grid, graph, artist, debug_info):
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
