from state import State
from main_menu import MainMenu
from settings import *
#from zone import Zone

class Title(State):
	def __init__(self, game):
		State.__init__(self, game)

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
		self.bigger_font = pygame.font.Font(FONT, 70)
		self.smaller_font = pygame.font.Font(FONT, 30)
		self.big_font = pygame.font.Font(FONT, 40)

		# continue box
		self.button_surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.1))
		self.continue_button_surf = self.button_surf
		self.continue_button_surf.fill(BLACK)
		self.continue_button_surf.set_alpha(self.alpha)
		self.continue_button_rect = self.continue_button_surf.get_rect(center = (HALF_WIDTH, HEIGHT * 0.8))

	def hover_and_click(self, display):

		if self.alpha >= 200:
			self.game.screen.blit(self.continue_button_surf, self.continue_button_rect)
			self.continue_button_surf.set_alpha(self.alpha)
			
			self.mx, self.my = pygame.mouse.get_pos()

			if self.continue_button_rect.collidepoint(self.mx, self.my):
				pygame.draw.rect(display, WHITE, self.continue_button_rect)
				self.continue_colour = BLACK
				if pygame.mouse.get_pressed()[0] == 1 and not self.fading:
					self.fading = True

			else:
				self.continue_colour = WHITE

			self.render_text('Start Game', self.continue_colour, self.smaller_font, (self.continue_button_rect.center))


	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def update(self):
		self.alpha += 5
		if self.alpha >= 200:
			self.alpha = 200

		# fadeout
		if self.fading:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				new_state = MainMenu(self.game)
				new_state.enter_state()

		# if actions['return']:
		# 	new_state = Zone(self.game)
		# 	new_state.enter_state()
		# self.game.reset_keys()

	def render(self, display):

		display.fill(BLUE)

		self.hover_and_click(self.game.screen)
		
		self.game.screen.blit(self.fade_surf, self.fade_rect)
		self.fade_surf.set_alpha(self.fadeout_alpha)

