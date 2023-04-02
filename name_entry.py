import pygame, csv, re
from state import State
from leaderboard import Leaderboard
from settings import *

class NameEntry(State):
	def __init__(self, game, level):
		State.__init__(self, game)

		self.game = game
		self.level = level
		self.mx, self.my = (0,0)
		self.state = ''
		self.alpha = 0
		self.fading = False
		self.no_name_entered = False

		#box
		self.box_surf = pygame.Surface(RES/2)
		self.box_surf.fill(BLACK)
		self.box_surf.set_alpha(self.alpha)
		self.box_rect = self.box_surf.get_rect(center = RES/2)

		# continue box
		self.button_surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.1))
		self.continue_button_surf = self.button_surf
		self.continue_button_surf.fill(BLACK)
		self.continue_button_surf.set_alpha(self.alpha)
		self.continue_button_rect = self.continue_button_surf.get_rect(center = (WIDTH * 0.8, HEIGHT * 0.2))
		
		# restart box
		self.restart_button_surf = self.button_surf
		self.restart_button_surf.fill(BLACK)
		self.restart_button_surf.set_alpha(self.alpha)
		self.restart_button_rect = self.restart_button_surf.get_rect(center = (WIDTH * 0.8, HEIGHT * 0.4))

		# bg
		self.background = self.game.get_image('assets/backgrounds/spots6.png', RES, RES/2)

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

			self.game.render_text('Continue', self.continue_colour, self.game.smaller_font, (self.continue_button_rect.center))
			self.game.render_text('Restart', self.restart_colour, self.game.smaller_font, (self.restart_button_rect.center))


	def update(self):
		self.game.player_name = re.sub(r"^\s+", "", self.game.player_name, flags=re.UNICODE)
		
		if self.game.player_name != '':
			self.no_name_entered = False

		if ACTIONS['return']:
			if self.game.player_name == '':
				self.no_name_entered = True
			else:
				self.game.name_entry_active = False

				# pass 'name entry' to leaderboard so it can append and show the new entry
				Leaderboard(self.game, self.level, self.level.car_type, 'Name Entry').enter_state()

		self.game.reset_keys()	

	def render(self, display):
		display.blit(self.background[0], self.background[1])

		display.blit(self.box_surf, self.box_rect)
		self.box_surf.set_alpha(self.alpha)

		self.alpha += 5
		if self.alpha >= 200:
			self.alpha = 200
			self.game.name_entry_active = True
		self.game.render_text(self.game.player_name, WHITE, self.game.small_font, (HALF_WIDTH, self.box_rect.top + self.box_surf.get_height()*0.66))
		self.game.render_text('Enter your name', WHITE, self.game.small_font, (HALF_WIDTH, self.box_rect.top + self.box_surf.get_height()*0.33))
		pygame.draw.line(self.game.screen, WHITE, (HALF_WIDTH - 30 * SCALE, self.box_rect.top + self.box_surf.get_height()*0.75), (HALF_WIDTH + 30 * SCALE, self.box_rect.top + self.box_surf.get_height()*0.75), SCALE)

		if self.no_name_entered:
			self.game.render_text('Enter a name!', PINK, self.game.small_font, (HALF_WIDTH, self.box_rect.top + self.box_surf.get_height()*0.9))

