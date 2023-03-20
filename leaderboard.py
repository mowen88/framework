import pygame
from state import State
from settings import *

class Leaderboard(State):
	def __init__(self, game, level, track_leaderboard):
		State.__init__(self, game)
		
		self.game = game
		self.level = level
		self.track_leaderboard = track_leaderboard
		self.leaderboard_height = ((HEIGHT * 0.075) * len(self.track_leaderboard)) - HEIGHT
		self.mx, self.my = (0,0)
		self.alpha = 0

		#fade surf
		self.fading = False
		self.fadeout_alpha = 0
		self.fade_surf = pygame.Surface(RES)
		self.fade_surf.fill(WHITE)
		self.fade_surf.set_alpha(self.fadeout_alpha)
		self.fade_rect = self.fade_surf.get_rect(center = RES/2)
		
		#font
		self.small_font = pygame.font.Font(FONT, 50)
		self.big_font = pygame.font.Font(FONT, 70)
		self.smaller_font = pygame.font.Font(FONT, 20)
		self.bigger_font = pygame.font.Font(FONT, 40)

		# images
		self.gold = pygame.image.load('assets/cups/gold.png').convert_alpha()
		self.silver = pygame.image.load('assets/cups/silver.png').convert_alpha()
		self.bronze = pygame.image.load('assets/cups/bronze.png').convert_alpha()

		# continue box
		self.button_surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.1))
		self.continue_button_surf = self.button_surf
		self.continue_button_surf.fill(BLACK)
		self.continue_button_surf.set_alpha(self.alpha)
		self.continue_button_rect = self.continue_button_surf.get_rect(center = (WIDTH * 0.75, HEIGHT * 0.5))

		#text boxes
		self.box_size = (180 * SCALE, 13 * SCALE)
		self.grey_box = pygame.Surface(self.box_size)
		self.grey_box.fill(BLACK)
		self.grey_box.set_alpha(self.alpha)
		self.grey_box_rect = self.grey_box.get_rect(center = RES/2)

		self.white_box = pygame.Surface(self.box_size)
		self.white_box.fill(WHITE)
		self.white_box_rect = self.white_box.get_rect(center = RES/2)

		# get starting scroll position at point of current players fastest lap
		self.scroll = self.get_start_scroll_pos()

	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def get_start_scroll_pos(self):
		for row in range(len(self.track_leaderboard)):
			if self.game.player_name in self.track_leaderboard[row] and self.game.fastest_lap in self.track_leaderboard[row]:
				if row > 8 and row < len(self.track_leaderboard) - 7:
					scroll = (HEIGHT * 0.075 * row - HALF_HEIGHT + (self.grey_box.get_height())) *-1
				elif row <= 8:
					scroll = SCALE
				else:
					scroll = -self.leaderboard_height - (HEIGHT * 0.075) - SCALE

				return scroll

	def hover_and_click(self, display):
		if self.alpha >= 200:
			self.mx, self.my = pygame.mouse.get_pos()

			if self.continue_button_rect.collidepoint(self.mx, self.my):
				pygame.draw.rect(display, WHITE, self.continue_button_rect)
				self.continue_colour = BLACK
				if pygame.mouse.get_pressed()[0] == 1 and not self.fading:
					self.fading = True

			else:
				self.continue_colour = WHITE

			self.render_text('Main Menu', self.continue_colour, self.smaller_font, (self.continue_button_rect.center))
		
	def show_list(self):
		start_height = 14 * SCALE
		
		for row in range(len(self.track_leaderboard)):
			
			index = self.track_leaderboard[row][0]
			name = str(self.track_leaderboard[row][1]).strip()
			lap = self.track_leaderboard[row][2]
			lap_above = self.track_leaderboard[row-1][2]
			track = self.track_leaderboard[row][3]
			car = self.track_leaderboard[row][4]
			direction = self.track_leaderboard[row][5]

			self.game.screen.blit(self.grey_box, (WIDTH * 0.3 - (self.grey_box.get_width()/2), self.scroll + start_height + HEIGHT * 0.075 * row))
			self.grey_box.set_alpha(self.alpha)

			if row < len(self.track_leaderboard) and self.alpha >= 200:
				self.render_text(f'{index}   |   {name}   |   {lap}   |   {car}   |   {direction}', WHITE, self.smaller_font, (WIDTH * 0.3, (self.grey_box.get_height()/2) + self.scroll + start_height + HEIGHT * 0.075 * row))
			
			if self.game.player_name in self.track_leaderboard[row] and self.game.fastest_lap in self.track_leaderboard[row]:
				self.game.screen.blit(self.white_box, (WIDTH * 0.3 - (self.grey_box.get_width()/2), self.scroll + start_height + HEIGHT * 0.075 * row))
				self.render_text(f'{index}   |   {name}   |   {lap}   |   {car}   |   {direction}', BLACK, self.smaller_font, (WIDTH * 0.3, (self.grey_box.get_height()/2) + self.scroll + start_height + HEIGHT * 0.075 * row))
			
			self.game.screen.blit(self.white_box, (WIDTH * 0.3 - (self.grey_box.get_width()/2), 0))
			pygame.draw.line(self.game.screen, BLACK, ((WIDTH * 0.3 - (self.grey_box.get_width()/2), self.grey_box.get_height())), ((WIDTH * 0.3 + (self.grey_box.get_width()/2), self.grey_box.get_height())), SCALE//2)
			self.render_text('Position  |   Name   |   Lap Time   |   Car   |    Track reversed?', BLACK, self.smaller_font, (WIDTH * 0.3, (self.grey_box.get_height()/2)))

			# render cups for 1st, 2nd and 3rd
			if row == 0 and self.alpha >= 200:
				self.game.screen.blit(self.gold, (WIDTH * 0.3 - (self.grey_box.get_width()/2) + (4* SCALE), (self.grey_box.get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))
				self.game.screen.blit(self.gold, (WIDTH * 0.3 + (self.grey_box.get_width()/2) - (4* SCALE) - self.gold.get_width(), (self.grey_box.get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))
			if row == 1 and self.alpha >= 200:
				self.game.screen.blit(self.silver, (WIDTH * 0.3 - (self.grey_box.get_width()/2) + (4* SCALE), (self.grey_box.get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))
				self.game.screen.blit(self.silver, (WIDTH * 0.3 + (self.grey_box.get_width()/2) - (4* SCALE) - self.silver.get_width(), (self.grey_box.get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))
			if row == 2 and self.alpha >= 200:
				self.game.screen.blit(self.bronze, (WIDTH * 0.3 - (self.grey_box.get_width()/2) + (4* SCALE), (self.grey_box.get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))
				self.game.screen.blit(self.bronze, (WIDTH * 0.3 + (self.grey_box.get_width()/2) - (4* SCALE) - self.bronze.get_width(), (self.grey_box.get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))

	def update(self):
		self.alpha += 5
		if self.alpha >= 200:
			self.alpha = 200
			if ACTIONS['scroll_up'] and self.scroll <= 0:
				self.scroll += HEIGHT * 0.05
			if ACTIONS['scroll_down'] and self.scroll >= -self.leaderboard_height - (HEIGHT * 0.075):
				self.scroll -= HEIGHT * 0.05
			self.game.reset_keys()

	def render(self, display):
		display.fill(WHITE)
		
		self.show_list()

		self.game.screen.blit(self.continue_button_surf, self.continue_button_rect)
		self.continue_button_surf.set_alpha(self.alpha)
		
		self.hover_and_click(self.game.screen)

		# fadeout and next state
		self.game.screen.blit(self.fade_surf, self.fade_rect)
		self.fade_surf.set_alpha(self.fadeout_alpha)

		if self.fading:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				self.prev_state.exit_state()
				self.prev_state.exit_state()
				self.level.exit_state()
				self.exit_state()
				
				
		
					
			


		
		
		