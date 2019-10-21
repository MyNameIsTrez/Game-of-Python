import pygame


class Artist:
	def __init__(self, screen, width, height):
		self.screen = screen
		self.width = width
		self.height = height

		self.outer_background_color = ((25, 25, 25))
		self.inner_background_color = (50, 50, 50)

	def fill_screen(self):
		# draw the outer background color
		self.screen.fill(self.outer_background_color)

		# draw the inner background color
		color = self.inner_background_color
		x = self.offset[0]
		y = self.offset[1]
		width = self.width
		height = self.height
		thickness = 0  # 0 means fill

		pygame.draw.rect(
			self.screen, color, (x, y, width, height), thickness
		)

	def rect(self, color, x, y, width, height, thickness):
		pygame.draw.rect(
			self.screen, color, (x, y, width, height), thickness
		)
