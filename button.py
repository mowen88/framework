import pygame
from settings import *

class Button:
	def __init__(self, colour, pos):
		self.image = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.09))
		self.image.fill(colour)
		self.rect = self.image.get_rect(center = pos)

		self.mx, self.my = pygame.mouse.get_pos()
		self.state = ''
		self.alpha = 0

	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def get_button(self, name, text_colour, button_colour, pos):
		surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.09))
		colour = text_colour
		surf.fill(button_colour)
		surf.set_alpha(self.alpha)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def hover(self, button_colour, text_colour, font, state, display):
		if self.rect.collidepoint(self.mx, self.my):
			pygame.draw.rect(display, button_colour, self.rect)
			self.render_text(state, text_colour, font, (self.rect.center))
			if pygame.mouse.get_pressed()[0] == 1:
				return state


