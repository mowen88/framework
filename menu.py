import pygame, csv

from state import State
from level import Level
from leaderboard import Leaderboard
from settings import *

#from zone import Zone

class Menu(State):
	def __init__(self, game, level):
		State.__init__(self, game)

		self.level = Level(self.game)
		self.track_leaderboard = []

		# reset leaderboard and player name
		self.game.player_name = ''
		LEADERBOARD_DATA.clear()
		self.game.get_leaderboard()

		for index, entry in enumerate(LEADERBOARD_DATA):
			if self.game.track in entry:
				self.track_leaderboard.append(entry)

		LEADERBOARD_DATA.sort(key = lambda LEADERBOARD_DATA: LEADERBOARD_DATA[1])
		self.track_leaderboard.sort(key = lambda LEADERBOARD_DATA: LEADERBOARD_DATA[1])

		for index, row in enumerate(self.track_leaderboard):
			row.insert(0, index + 1)

		LEADERBOARD_DATA.sort(key = lambda LEADERBOARD_DATA: LEADERBOARD_DATA[2])
		self.track_leaderboard.sort(key = lambda LEADERBOARD_DATA: LEADERBOARD_DATA[2])


		# button conditions, fade in and state
		self.state = ''
		self.alpha = 0

		# fade out surf
		self.fading_out = False
		self.fadeout_alpha = 0
		self.fade = self.fadeout(WHITE, self.fadeout_alpha)

		# background
		self.background = self.game.get_image('assets/backgrounds/i-pace.png', RES, RES/2)

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
				if self.state == 'Race':
					self.level.enter_state()
				if self.state == 'Leaderboard':
					Leaderboard(self.game, self.level, 'Menu').enter_state()

	def render(self, display):
		display.blit(self.background[0], self.background[1])

		self.game.render_text('Main Menu', WHITE, self.game.bigger_font, (HALF_WIDTH, HEIGHT /4))

		self.render_button('Race', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.4))
		self.render_button('Leaderboard', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.5))
		self.render_button('Controls', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.6))
		self.render_button('Quit', WHITE, BLACK, WHITE, (HALF_WIDTH, HEIGHT * 0.7))

		display.blit(self.fade[0], self.fade[1])
		self.fade[0].set_alpha(self.fadeout_alpha)

		
				
