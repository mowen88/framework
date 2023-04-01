import pygame
from state import State
from settings import *

class PauseMenu(State):
	def __init__(self, game, car, track):
		State.__init__(self, game)

		self.game = game
		self.car = car
		self.track = track
	
		# button conditions, fade in and state
		self.state = ''
		self.alpha = 200

		# fade out surf
		self.fading_out = False
		self.fadeout_alpha = 0
		self.fade = self.fadeout(WHITE, self.fadeout_alpha)

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
					if self.state == 'Main Menu':
						self.fading_out = True
					elif self.state == 'Retry':
						self.prev_state.exit_state()
						self.exit_state()
						self.game.create_level(self.car, self.track)
					else:
						self.prev_state.timer.stopstart()
						self.exit_state()

	def unpause(self):
		if ACTIONS['space']:
			self.prev_state.timer.stopstart()
			self.exit_state()
		self.game.reset_keys()
				
	def update(self):	
		self.unpause()

		if self.fading_out:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				self.prev_state.exit_state()
				self.prev_state.exit_state()
				self.prev_state.exit_state()
				self.exit_state()

	def render(self, display):
		self.prev_state.render(display)

		self.game.render_text('Paused', WHITE, self.game.bigger_font, (HALF_WIDTH, HEIGHT * 0.45))

		self.render_button('Continue', WHITE, BLACK, WHITE, (WIDTH * 0.3, HEIGHT * 0.6))
		self.render_button('Retry', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.6))
		self.render_button('Main Menu', WHITE, BLACK, WHITE, (WIDTH * 0.7, HEIGHT * 0.6))

		display.blit(self.fade[0], self.fade[1])
		self.fade[0].set_alpha(self.fadeout_alpha)
		
		