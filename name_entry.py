import pygame, csv
from state import State
from leaderboard import Leaderboard
from settings import *

class NameEntry(State):
	def __init__(self, game):

		State.__init__(self, game)
		self.game = game
		self.mx, self.my = (0,0)
		self.alpha = 0
		self.state = ''
		self.alpha = 0
		self.fading = False

		#font
		self.small_font = pygame.font.Font(FONT, 50)
		self.big_font = pygame.font.Font(FONT, 70)
		self.smaller_font = pygame.font.Font(FONT, 30)
		self.bigger_font = pygame.font.Font(FONT, 40)

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
			self.render_text('Restart', self.restart_colour, self.smaller_font, (self.restart_button_rect.center))


	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def update(self):

		if ACTIONS['return']:
			self.game.name_entry_active = False
						
			if len(self.game.player_name) <= 1:
				self.game.player_name = '???'

			new_leaderboard_entry = [self.game.player_name, self.game.fastest_lap, self.game.track, self.game.car_type, self.game.reverse_direction]
			LEADERBOARD_DATA.append(new_leaderboard_entry)

			LEADERBOARD_DATA.sort(key = lambda LEADERBOARD_DATA: LEADERBOARD_DATA[1])
			print(LEADERBOARD_DATA)

			with open('leaderboard.csv', 'a') as leaderboard_file:
				csv.writer(leaderboard_file).writerow(new_leaderboard_entry)
		
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


