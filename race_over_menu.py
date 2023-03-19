import pygame
from name_entry import NameEntry
from settings import *

class RaceOver:
	def __init__(self, game):

		self.game = game
		self.mx, self.my = (0,0)
		self.alpha = 0
		self.state = ''

		self.continue_colour = WHITE
		self.restart_colour = WHITE

		#fade surf
		self.fading = False
		self.fadeout_alpha = 0
		self.fade_surf = pygame.Surface(RES)
		self.fade_surf.fill(WHITE)
		self.fade_surf.set_alpha(self.fadeout_alpha)
		self.fade_rect = self.fade_surf.get_rect(center = RES/2)

		#font
		self.small_font = pygame.font.Font(FONT, 50)
		self.bigger_font = pygame.font.Font(FONT, 110)
		self.smaller_font = pygame.font.Font(FONT, 30)
		self.big_font = pygame.font.Font(FONT, 40)

		# for swipe up text and fade in of buttons
		self.y_pos = WIDTH + (5 * SCALE)
		

		# continue box
		self.button_surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.1))
		self.continue_button_surf = self.button_surf
		self.continue_button_surf.fill(BLACK)
		self.continue_button_surf.set_alpha(self.alpha)
		self.continue_button_rect = self.continue_button_surf.get_rect(center = (WIDTH * 0.4, HEIGHT * 0.65))
		# restart box
		self.restart_button_surf = self.button_surf
		self.restart_button_surf.fill(BLACK)
		self.restart_button_surf.set_alpha(self.alpha)
		self.restart_button_rect = self.restart_button_surf.get_rect(center = (WIDTH * 0.6, HEIGHT * 0.65))

	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def hover_and_click(self, display):
		mouse = pygame.mouse.get_pressed(num_buttons=5)

		if self.alpha >= 200:
			self.mx, self.my = pygame.mouse.get_pos()

			if self.continue_button_rect.collidepoint(self.mx, self.my) or self.state == 'continue':
				pygame.draw.rect(display, WHITE, self.continue_button_rect)
				self.continue_colour = BLACK
				if pygame.mouse.get_pressed()[0] == 1 and not self.fading:
					self.state = 'continue'
					self.fading = True

			elif self.restart_button_rect.collidepoint(self.mx, self.my) or self.state == 'restart':
				pygame.draw.rect(display, WHITE, self.restart_button_rect)
				self.restart_colour = BLACK
				if pygame.mouse.get_pressed()[0] == 1 and not self.fading:
					self.state = 'restart'
					self.fading = True
			else:
				self.continue_colour = WHITE
				self.restart_colour = WHITE

			self.render_text('Continue', self.continue_colour, self.smaller_font, (self.continue_button_rect.center))
			self.render_text('Retry', self.restart_colour, self.smaller_font, (self.restart_button_rect.center))


	def update(self, level):
		
		self.render_text('Race Over', WHITE, self.bigger_font, (HALF_WIDTH, self.y_pos))

		self.y_pos -= 20
		if self.y_pos <= HEIGHT * 0.45:
			self.y_pos = HEIGHT * 0.45
			self.alpha += 5
			if self.alpha >= 200:
				self.alpha = 200

		self.game.screen.blit(self.continue_button_surf, self.continue_button_rect)
		self.continue_button_surf.set_alpha(self.alpha)
		self.game.screen.blit(self.restart_button_surf, self.restart_button_rect)
		self.restart_button_surf.set_alpha(self.alpha)
		
		self.hover_and_click(self.game.screen)

		# fadeout and next state
		self.game.screen.blit(self.fade_surf, self.fade_rect)
		self.fade_surf.set_alpha(self.fadeout_alpha)

		if self.fading:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				if self.state == 'continue':
					new_state = NameEntry(self.game, level)
					new_state.enter_state()
				else:
					self.game.create_level()
			
		

		
			

