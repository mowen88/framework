import pygame, csv

from state import State
from entity import StackedSprite
from level import Level
from leaderboard import Leaderboard
from settings import *

#from zone import Zone

class CarTrackSelect(State):
	def __init__(self, game, level):
		State.__init__(self, game)


		self.track_leaderboard = []

		self.state = ''
		self.alpha = 0

		#vars
		self.laps = self.game


		self.cars = list(CAR_DATA.keys())
		self.tracks = list(TRACK_DATA.keys())
		
		self.car_index = self.cars[self.cars.index(self.game.car_type)]
		self.track_index = self.tracks[self.tracks.index(self.game.track)]
		
		
		self.car_index = 0
		self.car_str = self.cars[self.car_index]

		self.level = Level(self.game, self.car_str)

		# fade out surf
		self.fading_out = False
		self.fadeout_alpha = 0
		self.fade = self.fadeout(WHITE, self.fadeout_alpha)

		# track select box
		self.track_box = self.get_box((WIDTH * 0.35, HEIGHT * 0.8), BLACK, self.alpha, (WIDTH * 0.3, HALF_HEIGHT))
		self.car_box = self.get_box((WIDTH * 0.35, HEIGHT * 0.6), BLACK, self.alpha, (WIDTH * 0.7, HEIGHT * 0.4))

		# background
		self.background = self.game.get_image('assets/backgrounds/i-pace.png', RES, RES/2)

		# import classes
		self.car = StackedSprite(self.game, level, self.car_str, (WIDTH * 0.62, HEIGHT * 0.28), 90)
		self.track_surf = pygame.image.load(f'assets/tracks/{self.track_index}/minimap.png').convert_alpha()
		self.track_surf = pygame.transform.scale(self.track_surf, (self.track_surf.get_width()/SCALE, self.track_surf.get_height()/SCALE))
		self.track_rect = self.track_surf.get_rect(center = (self.track_box[1].centerx, self.track_box[1].centery - (HEIGHT * 0.1)))


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

	def get_box(self, size, colour, alpha, pos):
		size = size
		surf = pygame.Surface(size)
		surf.fill(colour)
		surf.set_alpha(alpha)
		rect = surf.get_rect(center = pos)
		return(surf, rect)

	def render_arrow(self, text_colour, pos, direction, state):
		surf = pygame.Surface((WIDTH * 0.05, HEIGHT * 0.09))
		colour = text_colour
		rect = surf.get_rect(center = pos)
		if direction == 'left':
			self.game.render_text('<', text_colour, self.game.small_font, pos)
		else:
			self.game.render_text('>', text_colour, self.game.small_font, pos)

		mx, my = pygame.mouse.get_pos()

		if self.alpha >= 200:
			if rect.collidepoint(mx, my):
				pygame.draw.circle(self.game.screen, WHITE, (rect.centerx, rect.centery + SCALE), 7 * SCALE)
				if direction == 'left':
					self.game.render_text('<', BLACK, self.game.small_font, pos)
				else:
					self.game.render_text('>', BLACK, self.game.small_font, pos)

				if ACTIONS['left_click'] and not self.fading_out:
					if direction == 'left':
						self.car_index -= 1
						if self.car_index < 0:
							self.car_index = len(self.cars)-1
					else:
						self.car_index += 1
						if self.car_index > len(self.cars) -1:
							self.car_index = 0

					state = self.cars[self.car_index]
					self.car.kill()
					self.car = StackedSprite(self.game, self.level, state, (WIDTH * 0.62, HEIGHT * 0.28), 90)

				self.game.reset_keys()


	def render_button(self, state, text_colour, button_colour, hover_colour, pos):
		surf = pygame.Surface((WIDTH * 0.35, HEIGHT * 0.15))
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
		self.car_str = self.cars[self.car_index]
		self.car.update()
		self.fadein()
		if self.fading_out:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				if self.state == 'Race':
					Level(self.game, self.car_str).enter_state()

	def render(self, display):
		display.blit(self.background[0], self.background[1])


		display.blit(self.track_box[0], self.track_box[1])
		self.track_box[0].set_alpha(self.alpha)
		display.blit(self.car_box[0], self.car_box[1])
		self.car_box[0].set_alpha(self.alpha)

		self.game.render_text('Track Select', WHITE, self.game.big_font, (WIDTH * 0.3, HEIGHT * 0.2))
		self.game.render_text('Car Select', WHITE, self.game.big_font, (WIDTH * 0.7, HEIGHT * 0.2))
		self.render_button('Race', WHITE, BLACK, WHITE, (WIDTH * 0.7, HEIGHT * 0.825))

		# show track
		display.blit(self.track_surf, self.track_rect)
		
		# show car
		
		self.car.image = pygame.transform.scale(self.car.image, (self.car.image.get_width()*1.5, self.car.image.get_height()*1.5))
		display.blit(self.car.image, self.car.pos)
		self.car.angle += 2

		# display.blit(self.left_black_icon[0], (WIDTH * 0.85, HEIGHT * 0.4))
		# self.left_black_icon[0].set_alpha(self.alpha)
		# self.right_black_icon = pygame.transform.flip(self.left_black_icon[0], True, False)
		# display.blit(self.right_black_icon, (WIDTH * 0.55, HEIGHT * 0.4))
		# self.right_black_icon.set_alpha(self.alpha)

		# car arrows
		self.game.render_text(self.car_str, WHITE, self.game.smaller_font, (self.car_box[1].centerx, self.car_box[1].bottom - (HEIGHT * 0.1)))
		self.render_arrow(WHITE, (self.car_box[1].left + (WIDTH * 0.03), self.car_box[1].centery), 'left', self.car_index)
		self.render_arrow(WHITE, (self.car_box[1].right - (WIDTH * 0.03), self.car_box[1].centery), 'right', self.car_index)

		#track arrows
		self.game.render_text(self.track_index, WHITE, self.game.smaller_font, (self.track_box[1].centerx, self.track_box[1].bottom - (HEIGHT * 0.3)))
		self.render_arrow(WHITE, (self.track_box[1].left + (WIDTH * 0.03), self.track_box[1].top + (HEIGHT * 0.3)), 'left', self.track_index)
		self.render_arrow(WHITE, (self.track_box[1].right - (WIDTH * 0.03), self.track_box[1].top + (HEIGHT * 0.3)), 'right', self.track_index)

		self.game.render_text('Laps', WHITE, self.game.smaller_font, (self.track_box[1].left + (WIDTH * 0.07), self.track_box[1].bottom - (HEIGHT * 0.2)))
		self.render_arrow(WHITE, (self.track_box[1].right - (WIDTH * 0.03), self.track_box[1].bottom - (HEIGHT * 0.2 + SCALE)), 'right', self.game.total_laps)
		self.render_arrow(WHITE, (self.track_box[1].right - (WIDTH * 0.13), self.track_box[1].bottom - (HEIGHT * 0.2 + SCALE)), 'left', self.game.total_laps)

		self.game.render_text('Reversed?', WHITE, self.game.smaller_font, (self.track_box[1].left + (WIDTH * 0.1), self.track_box[1].bottom - (HEIGHT * 0.1)))
		self.render_arrow(WHITE, (self.track_box[1].right - (WIDTH * 0.03), self.track_box[1].bottom - (HEIGHT * 0.1 + SCALE)), 'right', self.game.reverse_direction)
		self.render_arrow(WHITE, (self.track_box[1].right - (WIDTH * 0.13), self.track_box[1].bottom - (HEIGHT * 0.1 + SCALE)), 'left', self.game.reverse_direction)

		self.game.render_text(self.car_str, BLACK, self.game.small_font, RES/2)


		display.blit(self.fade[0], self.fade[1])
		self.fade[0].set_alpha(self.fadeout_alpha)
	

		
				
