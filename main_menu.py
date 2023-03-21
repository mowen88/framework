from state import State
from level import Level
from button import Button
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

		# bg
		self.bg = self.game.get_image('assets/backgrounds/i-pace.png', RES, RES/2)

	def get_button(self, state, text_colour, button_colour, hover_colour, pos):
		surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.09))
		colour = text_colour
		surf.fill(button_colour)
		surf.set_alpha(self.alpha)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)
		self.render_text(state, text_colour, self.smaller_font, pos)

		self.mx, self.my = pygame.mouse.get_pos()

		if rect.collidepoint(self.mx, self.my) or self.state == state:
			pygame.draw.rect(self.game.screen, hover_colour, rect)
			self.render_text(state, button_colour, self.smaller_font, pos)
			if pygame.mouse.get_pressed()[0] == 1 and not self.fading:
				self.state = state
				self.fading = True

	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def update(self):
		self.alpha += 5
		if self.alpha >= 200:
			self.alpha = 200

	def render(self, display):
		display.blit(self.bg[0], self.bg[1])

		self.get_button('Race', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.4))
		self.get_button('Leaderboard', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.5))
		self.get_button('Controls', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.6))
		self.get_button('Quit', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.7))

		display.blit(self.fade_surf, self.fade_rect)
		self.fade_surf.set_alpha(self.fadeout_alpha)

		# fadeout
		if self.fading:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				if self.state == 'Race':
					Level(self.game).enter_state()
				
