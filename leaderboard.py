import pygame
from state import State
from settings import *

class Leaderboard(State):
	def __init__(self, game):
		State.__init__(self, game)
		
		self.game = game

		#font
		self.small_font = pygame.font.Font(FONT, 50)
		self.big_font = pygame.font.Font(FONT, 70)
		self.smaller_font = pygame.font.Font(FONT, 20)
		self.bigger_font = pygame.font.Font(FONT, 40)

		#text boxes
		self.alpha = 0
		self.box_size = (180 * SCALE, 13 * SCALE)
		self.grey_box = pygame.Surface(self.box_size)
		self.grey_box.fill(BLACK)
		self.grey_box.set_alpha(self.alpha)
		self.grey_box_rect = self.grey_box.get_rect(center = RES/2)

		self.white_box = pygame.Surface(self.box_size)
		self.white_box.fill(WHITE)
		self.white_box_rect = self.white_box.get_rect(center = RES/2)

	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)
		
	def show_list(self):
		start_height = 10 * SCALE
		for row in range(len(LEADERBOARD_DATA)):

			name = str(LEADERBOARD_DATA[row][0]).strip()
			lap = LEADERBOARD_DATA[row][1]
			track = LEADERBOARD_DATA[row][2]
			car = LEADERBOARD_DATA[row][3]
			if LEADERBOARD_DATA[row][4]:
				direction = 'reversed'

			self.game.screen.blit(self.grey_box, (HALF_WIDTH - (self.grey_box.get_width()/2), start_height + HEIGHT * 0.075 * row))
			self.grey_box.set_alpha(self.alpha)
			if row < len(LEADERBOARD_DATA):
				self.render_text(f'Name: {name} Lap: {lap} Track: {track} Car: {car} Direction: {direction}', WHITE, self.smaller_font, (HALF_WIDTH, (self.grey_box.get_height()/2) + start_height + HEIGHT * 0.075 * row))
			if row == 5 and self.alpha >= 200:
				self.game.screen.blit(self.white_box, (HALF_WIDTH - (self.grey_box.get_width()/2), start_height + HEIGHT * 0.075 * row))
				self.render_text(f'Name: {self.game.player_name}', BLACK, self.smaller_font, (HALF_WIDTH, (self.grey_box.get_height()/2) + start_height + HEIGHT * 0.075 * row))
	
	def update(self):
		self.alpha += 5
		if self.alpha >= 200:
			self.alpha = 200

	def render(self, display):
		display.fill(WHITE)
		self.show_list()
		
		
		