import pygame, json
from state import State
from leaderboard import Leaderboard
from settings import *

class NameEntry(State):
	def __init__(self, game):

		State.__init__(self, game)
		self.game = game

		#font
		self.small_font = pygame.font.Font(FONT, 50)
		self.big_font = pygame.font.Font(FONT, 70)
		self.smaller_font = pygame.font.Font(FONT, 30)
		self.bigger_font = pygame.font.Font(FONT, 40)

		#box
		self.alpha = 0
		self.box_surf = pygame.Surface(RES/2)
		self.box_surf.fill(BLACK)
		self.box_surf.set_alpha(self.alpha)
		self.box_rect = self.box_surf.get_rect(center = RES/2)


	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def update(self):

		if ACTIONS['return']:
			self.game.name_entry_active = False
		
			

			new_state = Leaderboard(self.game)
			new_state.enter_state()

		self.game.reset_keys()	

	def render(self, display):
		display.fill(WHITE)

		display.blit(self.box_surf, self.box_rect)
		self.box_surf.set_alpha(self.alpha)

		self.alpha += 5
		if self.alpha >= 200:
			self.alpha = 200
			self.game.name_entry_active = True
		self.render_text(self.game.player_name, WHITE, self.small_font, (HALF_WIDTH, self.box_rect.top + self.box_surf.get_height()*0.66))
		self.render_text('Enter your name', WHITE, self.small_font, (HALF_WIDTH, self.box_rect.top + self.box_surf.get_height()*0.33))
		pygame.draw.line(self.game.screen, WHITE, (HALF_WIDTH - 30 * SCALE, self.box_rect.top + self.box_surf.get_height()*0.75), (HALF_WIDTH + 30 * SCALE, self.box_rect.top + self.box_surf.get_height()*0.75), SCALE)


