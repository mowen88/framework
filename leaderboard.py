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

			index = LEADERBOARD_DATA[row][0]
			name = str(LEADERBOARD_DATA[row][1]).strip()
			lap = LEADERBOARD_DATA[row][2]
			lap_above = LEADERBOARD_DATA[row-1][2]
			track = LEADERBOARD_DATA[row][3]
			car = LEADERBOARD_DATA[row][4]
			if LEADERBOARD_DATA[row][5]:
				direction = 'Reversed'
			else:
				direction = 'Normal'

			for i in lap_above:
				for j in lap:
					val = (str(j + i))
			print(val)

			self.game.screen.blit(self.grey_box, (HALF_WIDTH - (self.grey_box.get_width()/2), start_height + HEIGHT * 0.075 * row))
			self.grey_box.set_alpha(self.alpha)
			if row < len(LEADERBOARD_DATA) and self.alpha >= 200:
				self.render_text(f'{index}   |   {name}   |   {lap}   |   {car}   |   {direction}', WHITE, self.smaller_font, (HALF_WIDTH, (self.grey_box.get_height()/2) + start_height + HEIGHT * 0.075 * row))
			if self.game.player_name and self.game.fastest_lap in LEADERBOARD_DATA[row] or row == 0:
				self.game.screen.blit(self.white_box, (HALF_WIDTH - (self.grey_box.get_width()/2), start_height + HEIGHT * 0.075 * row))
				self.render_text(f'{index}   |   {name}   |   {lap}   |   {car}   |   {direction}', BLACK, self.smaller_font, (HALF_WIDTH, (self.grey_box.get_height()/2) + start_height + HEIGHT * 0.075 * row))
	
	def update(self):
		self.alpha += 5
		if self.alpha >= 200:
			self.alpha = 200

	def render(self, display):
		display.fill(WHITE)
		self.show_list()
		
		
		