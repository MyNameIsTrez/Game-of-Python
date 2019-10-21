import pygame


class Graph:
	def __init__(self, screen, width, height, artist):
		self.screen = screen
		self.width = width
		self.height = height
		self.artist = artist

		self.outer_background_color = ((25, 25, 25))
		self.inner_background_color = (50, 50, 50)
		self.data = []

	def draw(self):
		self.artist.fill_screen()
		for data in self.data:
			# print()
			for attr, value in data.items():
				# print(str(attr) + ": " + str(value))
				1 + 1
