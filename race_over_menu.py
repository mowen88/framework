import pygame
from name_entry import NameEntry
from settings import *

class RaceOver:
	def __init__(self, game, car, track):

		self.game = game
		self.car = car
		self.track = track
		self.alpha = 0
		self.state = ''

		# fade out surf
		self.fading_out = False
		self.fadeout_alpha = 0
		self.fade = self.fadeout(WHITE, self.fadeout_alpha)

		# for swipe up text and fade in of buttons
		self.y_pos = WIDTH + (5 * SCALE)

	def fadein(self):
		self.alpha += 5
		if self.alpha >= 200:
			self.alpha = 200

	def swipe_in(self):
		self.y_pos -= 20
		if self.y_pos <= HEIGHT * 0.45:
			self.y_pos = HEIGHT * 0.45

	def fadeout(self, colour, alpha):
		surf = pygame.Surface(RES)
		surf.fill(colour)
		surf.set_alpha(alpha)
		rect = surf.get_rect(center = RES/2)
		return(surf, rect)

	def render_button(self, state, text_colour, button_colour, hover_colour, pos):
		surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.09))
		colour = text_colour
		surf.fill(button_colour)
		surf.set_alpha(self.alpha)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)
		self.game.render_text(state, text_colour, self.game.smaller_font, pos)

		mx, my = pygame.mouse.get_pos()

		if self.alpha >= 200:
			if rect.collidepoint(mx, my) or self.state == state:
				pygame.draw.rect(self.game.screen, hover_colour, rect)
				self.game.render_text(state, button_colour, self.game.smaller_font, pos)
				if pygame.mouse.get_pressed()[0] == 1 and not self.fading_out:
					self.state = state
					self.fading_out = True


	def update(self, level):

		# fade in boxes and swipe in header
		self.fadein()
		self.swipe_in()

		# Header text
		self.game.render_text('Race Over', WHITE, self.game.bigger_font, (HALF_WIDTH, self.y_pos))
		
		# buttons
		self.render_button('Continue', WHITE, BLACK, WHITE, (WIDTH * 0.4, HEIGHT * 0.65))
		self.render_button('Retry', WHITE, BLACK, WHITE, (WIDTH * 0.6, HEIGHT * 0.65))

		# fadeout and next state
		self.game.screen.blit(self.fade[0], self.fade[1])
		self.fade[0].set_alpha(self.fadeout_alpha)

		if self.fading_out:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				if self.state == 'Continue':
					NameEntry(self.game, level).enter_state()
				else:
					level.exit_state()
					self.game.create_level(self.car, self.track)
			
		

		
			

