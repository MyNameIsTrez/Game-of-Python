import pygame


class Artist:
	def __init__(self, screen, width, height, font_neighbor, font_debug):
		self.screen = screen
		self.width = width
		self.height = height
		self.font_neighbor = font_neighbor
		self.font_debug = font_debug

		self.font_color = (255, 50, 50)
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

		self.rect(color, x, y, width, height, thickness)

	def rect(self, color, x, y, width, height, thickness):
		pygame.draw.rect(
			self.screen, color, (x, y, width, height), thickness
		)

	def text(self, x, y, text, color, font):
		if font == "neighbor":
			font = self.font_neighbor
		elif font == "debug":
			font = self.font_debug
		font.render_to(self.screen, (x, y), text, color)
