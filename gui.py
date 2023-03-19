import pygame
from race_over_menu import RaceOver
from settings import *

class GUI:
	def __init__(self, game, level):
		self.game = game
		self.level = level
		self.scale_factor = 5

		#font
		self.small_font = pygame.font.Font(FONT, 48)
		self.big_font = pygame.font.Font(FONT, 70)
		self.smaller_font = pygame.font.Font(FONT, 30)
		self.bigger_font = pygame.font.Font(FONT, 40)

		#text boxes
		self.box_size = (50 * SCALE, 22 * SCALE)
		self.grey_box = pygame.Surface(self.box_size)
		self.grey_box.fill(BLACK)
		self.grey_box.set_alpha(200)
		self.white_box = pygame.Surface(self.box_size)
		self.white_box.fill(WHITE)

		# minimap image
		self.minimap_image = pygame.image.load(f'assets/tracks/{self.game.track}/minimap.png').convert_alpha()
		self.minimap_image = pygame.transform.scale(self.minimap_image, (self.minimap_image.get_width() / self.scale_factor, self.minimap_image.get_height() / self.scale_factor))
		self.minimap_rect = self.minimap_image.get_rect(topright = (WIDTH, 0))

		# player pos 
		self.pos_x = 0
		self.pos_y = 0

		#marker image
		self.marker_image = pygame.image.load(f'assets//marker.png').convert_alpha()
		self.marker_image = pygame.transform.scale(self.marker_image, (self.marker_image.get_width() * SCALE, self.marker_image.get_height() * SCALE))
		self.marker_rect = self.marker_image.get_rect()

		self.race_over_menu = RaceOver(self.game)

	def render_text(self, text, colour, font, pos, centralised):
		surf = font.render(str(text), True, colour)
		if centralised:
			rect = surf.get_rect(midtop = pos)
		else:
			rect = surf.get_rect(topleft = pos)
		self.game.screen.blit(surf, rect)

	def update(self):

		# render boxes for best and prev lap
		self.game.screen.blit(self.grey_box, (((WIDTH * 0.05) - (2 * SCALE)), HEIGHT * 0.05))
		self.game.screen.blit(self.white_box, (((WIDTH * 0.05) - (2 * SCALE)), HEIGHT * 0.18))
		self.render_text("Prev Lap", WHITE, self.smaller_font, (WIDTH * 0.05, HEIGHT * 0.05), False)
		self.render_text("Best Lap", BLACK, self.smaller_font, (WIDTH * 0.05, HEIGHT * 0.18), False)

		# render actual values for best and prev lap
		if not self.level.lap_times:
			self.render_text("-- : -- : ---", WHITE, self.bigger_font, (WIDTH * 0.05, HEIGHT * 0.1), False)
			self.render_text("-- : -- : ---", BLACK, self.bigger_font, (WIDTH * 0.05, HEIGHT * 0.23), False)
		else:
			self.render_text(f"{self.level.lap_times[-1]}", WHITE, self.bigger_font, (WIDTH * 0.05, HEIGHT * 0.1), False)
			self.render_text(f"{min(self.level.lap_times)}", BLACK, self.bigger_font, (WIDTH * 0.05, HEIGHT * 0.23), False)
		
		# render minimap and update marker position
		self.pos_x = (WIDTH - self.minimap_image.get_width()) + self.level.all_sprites.offset[0]/(self.scale_factor * SCALE)
		self.pos_y = 0 + self.level.all_sprites.offset[1]/(self.scale_factor * SCALE)
		self.marker_rect.topleft = (self.pos_x + (self.marker_image.get_width()/2), self.pos_y)
		self.game.screen.blit(self.minimap_image, self.minimap_rect)
		self.game.screen.blit(self.marker_image, self.marker_rect)

		# render current lap
		if not self.level.finished_race:
			self.render_text("Current Lap", WHITE, self.small_font, (WIDTH * 0.5, HEIGHT * 0.04), True)
			self.render_text(f"{self.level.timer.get_elapsed_time()}", WHITE, self.big_font, (WIDTH * 0.39, HEIGHT * 0.1), False)
		
		# render laps remaining
		if len(self.level.lap_times) >= self.level.total_laps:
			self.render_text(f"Lap {self.level.total_laps} of {self.level.total_laps}", WHITE, self.small_font, (((WIDTH * 0.05) - (2 * SCALE)), HEIGHT * 0.3), False)
			self.level.finished_race = True
			self.level.player.angle = self.level.player.momentum_direction
			self.game.fastest_lap = min(self.level.lap_times)
			self.race_over_menu.update(self.level)
	
		else:
			self.render_text(f"Lap {len(self.level.lap_times)+1} of {self.level.total_laps}", WHITE, self.small_font, (((WIDTH * 0.05) - (2 * SCALE)), HEIGHT * 0.3), False)
		
			
		