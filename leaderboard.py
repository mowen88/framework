import pygame, csv
from state import State
from entity import StackedSprite
from settings import *

class Leaderboard(State):
	def __init__(self, game, level, car, state_from):
		State.__init__(self, game)

		self.state_from = state_from
		self.game = game
		self.level = level
		self.car = car
		self.track_leaderboard = []
		self.scroll = 0
		
		# button conditions, fade in and state
		self.state = ''
		self.place = 0
		self.first_place_stats = {}
		self.alpha = 0

		# fade out surf
		self.fading_out = False
		self.fadeout_alpha = 0
		self.fade = self.fadeout(WHITE, self.fadeout_alpha)

		# images
		self.gold = pygame.image.load('assets/cups/gold.png').convert_alpha()
		self.silver = pygame.image.load('assets/cups/silver.png').convert_alpha()
		self.bronze = pygame.image.load('assets/cups/bronze.png').convert_alpha()

		#car sprite
		self.car_sprite = StackedSprite(self.game, self.level, self.car, (WIDTH * 0.75, HEIGHT * 0.55), 90)

		#text boxes
		self.grey_box = self.get_box(BLACK, self.alpha, (180 * SCALE, 13 * SCALE), RES/2)
		self.car_sprite_box = self.get_box(BLACK, self.alpha, (WIDTH * 0.18, WIDTH * 0.18), self.car_sprite.rect.bottomright)
		self.lap_record_box = self.get_box(BLACK, self.alpha, (WIDTH * 0.18, WIDTH * 0.18), (WIDTH * 0.8, HEIGHT * 0.65))
		self.white_box = self.get_box(WHITE, 255, (180 * SCALE, 13 * SCALE), RES/2)
		
		# background
		self.background = self.game.get_image('assets/backgrounds/spots5.png', RES, RES/2)


		self.tracks = list(TRACK_DATA.keys())
		self.track_index = 0
		self.track_str = self.tracks[self.track_index]
		self.track_surf = pygame.image.load(f'assets/tracks/{self.track_str}/minimap.png').convert_alpha()
		self.track_surf = pygame.transform.scale(self.track_surf, (self.track_surf.get_width()/SCALE, self.track_surf.get_height()/SCALE))
		self.track_rect = self.track_surf.get_rect(center = (WIDTH * 0.8, HEIGHT * 0.3))

		# append new leaderboard entry if from name entry state...
		if self.state_from == 'Name Entry':
			self.get_leaderboard(self.level.track)
		else:
			self.get_leaderboard(self.track_str)


	def get_box(self, colour, alpha, size, pos):
		surf = pygame.Surface(size)
		surf.fill(colour)
		surf.set_alpha(alpha)
		rect = surf.get_rect(center = pos)
		return(surf, rect)

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
				pygame.draw.circle(self.game.screen, WHITE, (rect.centerx - 3, rect.centery + SCALE), 7 * SCALE)
				if direction == 'left':
					self.game.render_text('<', BLACK, self.game.small_font, pos)
				else:
					self.game.render_text('>', BLACK, self.game.small_font, pos)

				if ACTIONS['left_click'] and not self.fading_out:

					if direction == 'left':
						self.track_index -= 1
						if self.track_index < 0:
							self.track_index = len(self.tracks)-1
					else:
						self.track_index += 1
						if self.track_index > len(self.tracks) -1:
							self.track_index = 0

					state = self.tracks[self.track_index]

					self.track_surf = pygame.image.load(f'assets/tracks/{state}/minimap.png').convert_alpha()
					self.track_surf = pygame.transform.scale(self.track_surf, (self.track_surf.get_width()/SCALE, self.track_surf.get_height()/SCALE))
					self.track_rect = self.track_surf.get_rect(center = (WIDTH * 0.8, HEIGHT * 0.3))
				
					self.track_leaderboard.clear()
					self.get_leaderboard(state)

				self.game.reset_keys()

	def get_leaderboard(self, track):

		if self.state_from == 'Name Entry':
			new_leaderboard_entry = [self.game.player_name, self.game.fastest_lap, track, self.car, self.game.reverse_direction]
			LEADERBOARD_DATA.append(new_leaderboard_entry)

			with open('leaderboard.csv', 'a') as leaderboard_file:
				csv.writer(leaderboard_file).writerow(new_leaderboard_entry)

		for row in LEADERBOARD_DATA:
			if len(row) >= 6:
				del row[0]

		LEADERBOARD_DATA.sort(key = lambda LEADERBOARD_DATA: LEADERBOARD_DATA[1])

		for index, row in enumerate(LEADERBOARD_DATA):
			row.insert(0, index + 1)

		#LEADERBOARD_DATA.sort(key = lambda LEADERBOARD_DATA: LEADERBOARD_DATA[2])

		for entry in LEADERBOARD_DATA:
			if track in entry: 
				self.track_leaderboard.append(entry)

		for index, j in enumerate(self.track_leaderboard):
			del j[0] 
			j.insert(0, index +1)

		self.leaderboard_height = ((HEIGHT * 0.075) * len(self.track_leaderboard)) - HEIGHT

		# start scroll position where the player is positioned
		for row in range(len(self.track_leaderboard)):
			name = self.track_leaderboard[row][1]
			lap = self.track_leaderboard[row][2]
			if name == str(self.game.player_name) and lap == self.game.fastest_lap:
				if row > 8 and row < len(self.track_leaderboard) - 7:
					self.scroll = -(self.grey_box[0].get_height() * (row - 6))
				elif row <= 8:
					self.scroll = SCALE
				else:
					self.scroll = -self.leaderboard_height

	def scrolling_logic(self):
		keys = pygame.key.get_pressed()

		if (ACTIONS['scroll_up'] or keys[pygame.K_UP]) and self.scroll < 0:
			self.scroll += HEIGHT * 0.05
			if self.scroll > 0:
				self.scroll = 0
		if (ACTIONS['scroll_down'] or keys[pygame.K_DOWN]) and self.scroll > -self.leaderboard_height - (HEIGHT * 0.075):
			self.scroll -= HEIGHT * 0.05
			if self.scroll < -self.leaderboard_height - (HEIGHT * 0.075):
				self.scroll = -self.leaderboard_height - (HEIGHT * 0.075)
		self.game.reset_keys()

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
		
	def show_list_of_entries(self):
		start_height = 14 * SCALE
		for row in range(len(self.track_leaderboard)):
			
			index = self.track_leaderboard[row][0]
			name = str(self.track_leaderboard[row][1]).strip()
			lap = self.track_leaderboard[row][2]
			lap_above = self.track_leaderboard[row-1][2]
			track = self.track_leaderboard[row][3]
			car = self.track_leaderboard[row][4]
			direction = self.track_leaderboard[row][5]

			self.game.screen.blit(self.grey_box[0], (WIDTH * 0.3 - (self.grey_box[0].get_width()/2), self.scroll + start_height + HEIGHT * 0.075 * row))
			self.grey_box[0].set_alpha(self.alpha)

			if row < len(self.track_leaderboard) and self.alpha >= 200:
				self.game.render_text(f'{index}    |    {name}    |    {lap}    |    {car}    |    {direction}', WHITE, self.game.even_smaller_font, (WIDTH * 0.3, (self.grey_box[0].get_height()/2) + self.scroll + start_height + HEIGHT * 0.075 * row))
			
			# white box for player's fastest lap if entering leaderboard from name entry state
			if self.game.player_name in self.track_leaderboard[row] and self.game.fastest_lap in self.track_leaderboard[row]:
				self.place = row + 1
				self.game.screen.blit(self.white_box[0], (WIDTH * 0.3 - (self.white_box[0].get_width()/2), self.scroll + start_height + HEIGHT * 0.075 * row))
				self.game.render_text(f'{index}    |    {name}    |    {lap}    |    {car}    |    {direction}', BLACK, self.game.even_smaller_font, (WIDTH * 0.3, (self.grey_box[0].get_height()/2) + self.scroll + start_height + HEIGHT * 0.075 * row))
			
			self.game.screen.blit(self.white_box[0], (WIDTH * 0.3 - (self.white_box[0].get_width()/2), 0))
			#pygame.draw.line(self.game.screen, WHITE, ((WIDTH * 0.3 - (self.white_box[0].get_width()/2), self.white_box[0].get_height())), ((WIDTH * 0.3 + (self.white_box[0].get_width()/2), self.white_box[0].get_height())), SCALE//2)
			self.game.render_text('Position   |    Name    |    Lap Time    |   Car    |     Track reversed?', BLACK, self.game.even_smaller_font, (WIDTH * 0.3, (self.white_box[0].get_height()/2)))

			# render cups for 1st, 2nd and 3rd
			if self.alpha >= 200:
				if row == 0:
					self.first_place_stats.update({'Name': name, 'Place': row, 'Lap': lap, 'Car': car, 'Direction': direction})
					self.game.screen.blit(self.gold, (WIDTH * 0.3 - (self.grey_box[0].get_width()/2) + (4* SCALE), (self.grey_box[0].get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))
					self.game.screen.blit(self.gold, (WIDTH * 0.3 + (self.grey_box[0].get_width()/2) - (4* SCALE) - self.gold.get_width(), (self.grey_box[0].get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))
				if row == 1:
					self.game.screen.blit(self.silver, (WIDTH * 0.3 - (self.grey_box[0].get_width()/2) + (4* SCALE), (self.grey_box[0].get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))
					self.game.screen.blit(self.silver, (WIDTH * 0.3 + (self.grey_box[0].get_width()/2) - (4* SCALE) - self.silver.get_width(), (self.grey_box[0].get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))
				if row == 2:
					self.game.screen.blit(self.bronze, (WIDTH * 0.3 - (self.grey_box[0].get_width()/2) + (4* SCALE), (self.grey_box[0].get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))
					self.game.screen.blit(self.bronze, (WIDTH * 0.3 + (self.grey_box[0].get_width()/2) - (4* SCALE) - self.bronze.get_width(), (self.grey_box[0].get_height()/SCALE) + self.scroll + start_height + HEIGHT * 0.075 * row))


	def update(self):
		# change track images, needs top be in update so click action works
		self.track_str = self.tracks[self.track_index]
		if self.state_from == 'Menu':
			self.render_arrow(WHITE, (self.track_rect.centerx - (WIDTH * 0.15), self.track_rect.centery), 'left', self.track_index)
			self.render_arrow(WHITE, (self.track_rect.centerx + (WIDTH * 0.15), self.track_rect.centery), 'right', self.track_index)

		self.car_sprite.update()
		self.scrolling_logic()
		self.fadein()

		if self.fading_out:
			self.fadeout_alpha += 255//50
			if self.fadeout_alpha >= 255:
				if self.state_from == 'Menu':
					self.exit_state()
					self.prev_state.exit_state()
				elif self.state_from == 'Name Entry':
					self.exit_state()
					self.prev_state.exit_state()
					self.prev_state.exit_state()
					self.prev_state.exit_state()
					self.prev_state.level.exit_state()
		
	def render(self, display):
		display.blit(self.background[0], self.background[1])

		display.blit(self.track_surf, self.track_rect)
		self.game.render_text(self.track_str, WHITE, self.game.small_font, (self.track_rect.centerx, HEIGHT * 0.1))

		#track arrows
		if self.state_from == 'Menu':
			self.render_arrow(WHITE, (self.track_rect.centerx - (WIDTH * 0.15), self.track_rect.centery), 'left', self.track_index)
			self.render_arrow(WHITE, (self.track_rect.centerx + (WIDTH * 0.15), self.track_rect.centery), 'right', self.track_index)
		
		self.show_list_of_entries()

		if self.state_from == 'Name Entry':
			self.render_button('Main Menu', WHITE, BLACK, WHITE, (self.car_sprite_box[1].centerx, HEIGHT * 0.9))

			display.blit(self.car_sprite_box[0], self.car_sprite_box[1])
			self.car_sprite_box[0].set_alpha(self.alpha)
			
			display.blit(self.car_sprite.image, self.car_sprite.pos)
			self.car_sprite.angle += 2
			if self.alpha >= 200:
				self.game.render_text(f'{self.place} / {len(self.track_leaderboard)}', WHITE, self.game.smaller_font, (self.car_sprite_box[1].centerx, self.car_sprite_box[1].bottom - (HEIGHT * 0.05)))

		else:
			self.render_button('Main Menu', WHITE, BLACK, WHITE, (WIDTH * 0.8, HEIGHT * 0.9))

			display.blit(self.lap_record_box[0], self.lap_record_box[1])
			self.lap_record_box[0].set_alpha(self.alpha)

			if self.alpha >= 200:
				pygame.draw.rect(display, WHITE, ((self.lap_record_box[1].topleft), (self.lap_record_box[1].width, self.lap_record_box[1].height * 0.3)))
				self.game.render_text('Lap Record', BLACK, self.game.smaller_font, (self.lap_record_box[1].centerx, self.lap_record_box[1].bottom - (self.lap_record_box[1].height * 0.85)))
				self.game.render_text(self.first_place_stats['Name'], WHITE, self.game.smaller_font, (self.lap_record_box[1].centerx, self.lap_record_box[1].bottom - (self.lap_record_box[1].height * 0.6)))
				self.game.render_text(self.first_place_stats['Lap'], WHITE, self.game.smaller_font, (self.lap_record_box[1].centerx, self.lap_record_box[1].bottom - (self.lap_record_box[1].height * 0.4)))
				self.game.render_text(self.first_place_stats['Car'], WHITE, self.game.smaller_font, (self.lap_record_box[1].centerx, self.lap_record_box[1].bottom - (self.lap_record_box[1].height * 0.2)))


		# fadeout and next state
		display.blit(self.fade[0], self.fade[1])
		self.fade[0].set_alpha(self.fadeout_alpha)

		

				
				
				
		
					
			


		
		
		