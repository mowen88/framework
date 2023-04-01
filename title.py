from state import State
from menu import Menu
from settings import *
#from zone import Zone

class Title(State):
	def __init__(self, game):
		State.__init__(self, game)

		# button conditions, fade in and state
		self.state = ''
		self.alpha = 0

		# fade out surf
		self.fading_out = False
		self.fadeout_alpha = 0
		self.fade = self.fadeout(WHITE, self.fadeout_alpha)

		# bg
		self.background = self.game.get_image('assets/backgrounds/gen3_front.png', RES, RES/2)

	def fadein(self):
		self.alpha += 5
		if self.alpha >= 200:
			self.alpha = 200

	def fadeout(self, colour, alpha):
		surf = pygame.Surface(RES)
		surf.fill(colour)
		surf.set_alpha(alpha)
		rect = surf.get_rect(center = RES/2)
		return(surf, rect)

	def render_button(self, state, text_colour, button_colour, hover_colour, pos):
		surf = pygame.Surface((WIDTH * 0.18, HEIGHT * 0.09))
		colour = text_colour
		surf.fill(button_colour)
		surf.set_alpha(self.alpha)
		rect = surf.get_rect(center = pos)
		self.game.screen.blit(surf, rect)
		self.game.render_text(state, text_colour, self.game.smaller_font, pos)

		mx, my = pygame.mouse.get_pos()

		if self.alpha >= 200:
			if rect.collidepoint(mx, my) or self.state == state:
				pygame.draw.rect(self.game.screen, hover_colour, rect)
				self.game.render_text(state, button_colour, self.game.smaller_font, pos)
				if pygame.mouse.get_pressed()[0] == 1 and not self.fading_out:
					self.state = state
					self.fading_out = True

	def update(self):
		self.fadein()
		if self.fading_out:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				if self.state == 'Start Game':
					Menu(self.game, None).enter_state()

		# if actions['return']:
		# 	new_state = Zone(self.game)
		# 	new_state.enter_state()
		# self.game.reset_keys()

	def render(self, display):
		#display.blit(self.background[0], self.background[1])
		display.fill(ORANGE)

		self.game.render_text('Racing Game', WHITE, self.game.bigger_font, (HALF_WIDTH, HEIGHT * 0.4))

		self.render_button('Start Game', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT *0.55))
		
		display.blit(self.fade[0], self.fade[1])
		self.fade[0].set_alpha(self.fadeout_alpha)




