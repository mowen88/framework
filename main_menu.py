from state import State
from level import Level
from settings import *
#from zone import Zone

class MainMenu(State):
	def __init__(self, game):
		State.__init__(self, game)


		self.game.player_name = ''
		LEADERBOARD_DATA.clear()
		self.game.get_leaderboard()

		self.mx, self.my = (0,0)
		self.state = ''
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
		self.bigger_font = pygame.font.Font(FONT, 70)
		self.smaller_font = pygame.font.Font(FONT, 30)
		self.big_font = pygame.font.Font(FONT, 40)

		#button surfs and text colours
		self.button_surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.09))

		self.race_colour = WHITE
		self.leaderboard_colour = WHITE
		self.controls_colour = WHITE
		self.quit_colour = WHITE

		# race box
		self.race_button_surf = self.button_surf
		self.race_button_surf.fill(BLACK)
		self.race_button_surf.set_alpha(self.alpha)
		self.race_button_rect = self.race_button_surf.get_rect(center = (HALF_WIDTH, HEIGHT * 0.4))

		# leaderboard box
		self.leaderboard_button_surf = self.button_surf
		self.leaderboard_button_surf.fill(BLACK)
		self.leaderboard_button_surf.set_alpha(self.alpha)
		self.leaderboard_button_rect = self.leaderboard_button_surf.get_rect(center = (HALF_WIDTH, HEIGHT * 0.5))

		# controls box
		self.controls_button_surf = self.button_surf
		self.controls_button_surf.fill(BLACK)
		self.controls_button_surf.set_alpha(self.alpha)
		self.controls_button_rect = self.controls_button_surf.get_rect(center = (HALF_WIDTH, HEIGHT * 0.6))

		# quit box
		self.quit_button_surf = self.button_surf
		self.quit_button_surf.fill(BLACK)
		self.quit_button_surf.set_alpha(self.alpha)
		self.quit_button_rect = self.quit_button_surf.get_rect(center = (HALF_WIDTH, HEIGHT * 0.7))

	def get_button(self, name, text_colour, button_colour, pos):
		surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.09))
		colour = text_colour
		surf.fill(button_colour)
		surf.set_alpha(self.alpha)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)
		return rect

	
	def hover_and_click(self, display):

		if self.alpha >= 200:
				
			self.mx, self.my = pygame.mouse.get_pos()

			if self.get_button('Race', BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.4)).collidepoint(self.mx, self.my) or self.state == 'Race':
				if pygame.mouse.get_pressed()[0] == 1 and not self.fading:
					self.state = 'Race'
					self.fading = True
			else:
				self.get_button('Race', WHITE, BLACK, (HALF_WIDTH, HEIGHT * 0.4))

			if self.leaderboard_button_rect.collidepoint(self.mx, self.my) or self.state == 'Leaderboard':
				pygame.draw.rect(display, WHITE, self.leaderboard_button_rect)
				self.leaderboard_colour = BLACK
				if pygame.mouse.get_pressed()[0] == 1 and not self.fading:
					self.state = 'Leaderboard'
					self.fading = True
			else:
				self.leaderboard_colour = WHITE

			if self.controls_button_rect.collidepoint(self.mx, self.my) or self.state == 'Controls':
				pygame.draw.rect(display, WHITE, self.controls_button_rect)
				self.controls_colour = BLACK
				if pygame.mouse.get_pressed()[0] == 1 and not self.fading:
					self.state = 'Controls'
					self.fading = True
			else:
				self.controls_colour = WHITE

			if self.quit_button_rect.collidepoint(self.mx, self.my) or self.state == 'Quit':
				pygame.draw.rect(display, WHITE, self.quit_button_rect)
				self.quit_colour = BLACK

				if pygame.mouse.get_pressed()[0] == 1 and not self.fading:
					self.state = 'Quit'
					self.fading = True
			else:
				self.quit_colour = WHITE

			self.render_text('Race', self.race_colour, self.smaller_font, (self.race_button_rect.center))
			self.render_text('Leaderboard', self.leaderboard_colour, self.smaller_font, (self.leaderboard_button_rect.center))
			self.render_text('Controls', self.controls_colour, self.smaller_font, (self.controls_button_rect.center))
			self.render_text('Quit Game', self.quit_colour, self.smaller_font, (self.quit_button_rect.center))


	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def update(self):
		self.alpha += 5
		if self.alpha >= 200:
			self.alpha = 200

		if ACTIONS['return']:
			new_state = Level(self.game)
			new_state.enter_state()
		self.game.reset_keys()

	def render(self, display):
		display.fill(WHITE)

		self.get_button('Race', WHITE, BLACK, (HALF_WIDTH, HEIGHT * 0.4))
		self.get_button('Leaderboard', WHITE, BLACK, (HALF_WIDTH, HEIGHT * 0.5))
		self.get_button('Controls', WHITE, BLACK, (HALF_WIDTH, HEIGHT * 0.6))
		self.get_button('Quit', WHITE, BLACK, (HALF_WIDTH, HEIGHT * 0.7))
		
		self.hover_and_click(self.game.screen)

	
		self.game.screen.blit(self.fade_surf, self.fade_rect)
		self.fade_surf.set_alpha(self.fadeout_alpha)

		# fadeout
		if self.fading:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				if self.state == 'Race':
					Level(self.game).enter_state()
				
