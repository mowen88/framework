import pygame, csv

from state import State
from entity import StackedSprite
from leaderboard import Leaderboard
from settings import *

#from zone import Zone

class CarTrackSelect(State):
	def __init__(self, game, level):
		State.__init__(self, game)

		self.level = level
		self.track_leaderboard = []

		self.state = ''
		self.alpha = 0

		#vars
		self.laps = self.game

		# fade out surf
		self.fading_out = False
		self.fadeout_alpha = 0
		self.fade = self.fadeout(WHITE, self.fadeout_alpha)

		# track select box
		self.grey_box = self.get_box(BLACK, self.alpha, (WIDTH * 0.25, HALF_HEIGHT))

		# background
		self.background = self.game.get_image('assets/backgrounds/i-pace.png', RES, RES/2)

		# import classes
		self.car = StackedSprite(self.game, self.level, self.game.car_type, (WIDTH * 0.65, HALF_HEIGHT), 90)
		self.track_surf = pygame.image.load(f'assets/tracks/{self.game.track}/minimap.png').convert_alpha()
		self.track_surf = pygame.transform.scale(self.track_surf, (self.track_surf.get_width()/SCALE, self.track_surf.get_height()/SCALE))
		self.track_rect = self.track_surf.get_rect(center = (self.grey_box[1].centerx, self.grey_box[1].centery - (HEIGHT * 0.1)))

		self.left_white_icon = self.game.get_image('assets/white_circle_icon.png', (64, 64), RES/2)
		self.left_black_icon = self.game.get_image('assets/black_circle_icon.png', (64, 64), (WIDTH * 0.2, HEIGHT * 0.7))
		self.left_black_icon[0].set_alpha(200)

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


	def get_box(self, colour, alpha, pos):
		size = (WIDTH * 0.4, HEIGHT * 0.8)
		surf = pygame.Surface(size)
		surf.fill(colour)
		surf.set_alpha(alpha)
		rect = surf.get_rect(center = pos)
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
		self.car.update()
		self.fadein()
		if self.fading_out:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				if self.state == 'Race':
					self.level.enter_state()

	def render(self, display):
		display.blit(self.background[0], self.background[1])


		display.blit(self.grey_box[0], self.grey_box[1])
		self.grey_box[0].set_alpha(self.alpha)

		self.game.render_text('Track Select', WHITE, self.game.big_font, (WIDTH * 0.25, HEIGHT * 0.2))


		# show track
		display.blit(self.track_surf, self.track_rect)
		
		# show car
		display.blit(self.car.image, self.car.pos)
		self.car.angle += 2

		display.blit(self.left_black_icon[0], self.left_black_icon[1])

		self.render_button('Race', WHITE, BLACK, WHITE, (WIDTH * 0.7, HEIGHT * 0.8))


		display.blit(self.fade[0], self.fade[1])
		self.fade[0].set_alpha(self.fadeout_alpha)
	

		
				
