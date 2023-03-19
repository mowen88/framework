import pygame
from state import State
from settings import *

class PauseMenu(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		self.mx, self.my = (0,0)
		self.alpha = 200

		self.continue_colour = WHITE
		self.restart_colour = WHITE
		self.main_menu_colour = WHITE

		#font
		self.small_font = pygame.font.Font(FONT, 50)
		self.bigger_font = pygame.font.Font(FONT, 110)
		self.smaller_font = pygame.font.Font(FONT, 30)
		self.big_font = pygame.font.Font(FONT, 40)

		# continue box
		self.button_surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.1))
		self.continue_button_surf = self.button_surf
		self.continue_button_surf.fill(BLACK)
		self.continue_button_surf.set_alpha(self.alpha)
		self.continue_button_rect = self.continue_button_surf.get_rect(center = (WIDTH * 0.3, HEIGHT * 0.6))
		# restart box
		self.restart_button_surf = self.button_surf
		self.restart_button_surf.fill(BLACK)
		self.restart_button_surf.set_alpha(self.alpha)
		self.restart_button_rect = self.restart_button_surf.get_rect(center = (WIDTH * 0.5, HEIGHT * 0.6))
		# main menu box
		self.main_menu_button_surf = self.button_surf
		self.main_menu_button_surf.fill(BLACK)
		self.main_menu_button_surf.set_alpha(self.alpha)
		self.main_menu_button_rect = self.main_menu_button_surf.get_rect(center = (WIDTH * 0.7, HEIGHT * 0.6))

	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def hover_and_click(self, display):
		mouse = pygame.mouse.get_pressed(num_buttons=5)

		self.mx, self.my = pygame.mouse.get_pos()

		if self.continue_button_rect.collidepoint(self.mx, self.my):
			pygame.draw.rect(display, WHITE, self.continue_button_rect)
			self.continue_colour = BLACK
			if pygame.mouse.get_pressed()[0] == 1:
				self.prev_state.timer.stopstart()
				self.exit_state()

		elif self.restart_button_rect.collidepoint(self.mx, self.my):
			pygame.draw.rect(display, WHITE, self.restart_button_rect)
			self.restart_colour = BLACK
			if pygame.mouse.get_pressed()[0] == 1:
				self.prev_state.exit_state()
				self.exit_state()
				self.game.create_level()

		elif self.main_menu_button_rect.collidepoint(self.mx, self.my):
			pygame.draw.rect(display, WHITE, self.main_menu_button_rect)
			self.main_menu_colour = BLACK
			if pygame.mouse.get_pressed()[0] == 1:
				self.prev_state.exit_state()
				self.prev_state.exit_state()
				self.exit_state()


		else:
			self.continue_colour = WHITE
			self.restart_colour = WHITE
			self.main_menu_colour = WHITE

		self.render_text('Continue', self.continue_colour, self.smaller_font, (self.continue_button_rect.center))
		self.render_text('Retry', self.restart_colour, self.smaller_font, (self.restart_button_rect.center))
		self.render_text('Main Menu', self.main_menu_colour, self.smaller_font, (self.main_menu_button_rect.center))

	def update(self):	
		if ACTIONS['space']:
			self.prev_state.timer.stopstart()
			self.exit_state()
		self.game.reset_keys()

	def render(self, display):
		self.prev_state.render(display)
		display.blit(self.continue_button_surf, self.continue_button_rect)
		self.continue_button_surf.set_alpha(self.alpha)

		display.blit(self.restart_button_surf, self.restart_button_rect)
		self.restart_button_surf.set_alpha(self.alpha)

		display.blit(self.main_menu_button_surf, self.main_menu_button_rect)
		self.main_menu_button_surf.set_alpha(self.alpha)
		
		self.hover_and_click(display)

		self.render_text('Paused', WHITE, self.bigger_font, (HALF_WIDTH, HEIGHT * 0.4))