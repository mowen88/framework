from state import State
from level import Level
from settings import *
#from zone import Zone

class Title(State):
	def __init__(self, game):
		State.__init__(self, game)

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


	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)

	def update(self):

		# fadeout
		if ACTIONS['space']:
			self.fading = True
		self.game.reset_keys()	

		if self.fading:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				new_state = Level(self.game)
				new_state.enter_state()

		# if actions['return']:
		# 	new_state = Zone(self.game)
		# 	new_state.enter_state()
		# self.game.reset_keys()

	def render(self, display):

		display.fill(BLUE)
		self.render_text('Press Space', BLACK, self.big_font, RES/2)
		self.game.screen.blit(self.fade_surf, self.fade_rect)
		self.fade_surf.set_alpha(self.fadeout_alpha)

