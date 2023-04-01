import pygame
from settings import *
from os import walk
from state import State
from camera import Camera
from entity import StackedSprite
from timer import Timer
from pause_menu import PauseMenu
from gui import GUI
from particles import Skidmarks, Dust, Shadow

class Level(State):
	def __init__(self, game, car, track):
		State.__init__(self, game)

		self.game = game
		self.car_type = car
		self.track = track
		self.friction = 0.4
		self.paused = False

		#fade surf
		self.fading = False
		self.fadein_alpha = 255
		self.fade_surf = pygame.Surface(RES)
		self.fade_surf.fill(WHITE)
		self.fade_surf.set_alpha(self.fadein_alpha)
		self.fade_rect = self.fade_surf.get_rect(center = RES/2)

		self.player_name = self.game.player_name
		self.total_laps = self.game.total_laps
		self.reverse_direction = self.game.reverse_direction
		
		self.started_race = False
		self.finished_race = False
		self.start_pos = TRACK_DATA[self.track]['start_pos']
		self.start_orientation = TRACK_DATA[self.track]['start_orientation']

		#images
		
		self.track_img = self.get_track_images('track')[0]

		self.track_border = self.get_track_images('track_border')[0]
		self.track_border_mask = self.get_track_images('track_border')[1]

		self.gravel_trap = self.get_track_images('gravel_trap')[0]
		self.gravel_trap_mask = self.get_track_images('gravel_trap')[1]
		
		if self.start_orientation['vert'] != 0:
			self.finish_line = self.get_track_images('finish_line_hori')[0]
			self.finish_line_mask = self.get_track_images('finish_line_hori')[1]
		else:
			self.finish_line = self.get_track_images('finish_line_vert')[0]
			self.finish_line_mask = self.get_track_images('finish_line_vert')[1]

		# checkpoints
		self.track_data = TRACK_DATA[self.track]['checkpoints']
		self.checkpoints = self.get_checkpoint_positions()
		self.passed_checkpoints = [-1]
		self.anti_cheat_reverse_checkpoints = []
		self.num_of_checkpoints = list(self.track_data.keys())[-1]
		self.lap_times = []

		# init player
		self.player_start_pos = self.get_player_start_pos_and_angle()[0]
		self.player_start_angle = self.get_player_start_pos_and_angle()[1]
		self.player = StackedSprite(self.game, self, self.car_type, self.player_start_pos, self.player_start_angle)

		# sprite groups
		self.floor_layer = pygame.sprite.Group()
		self.all_sprites = Camera(self.game, self)
		self.all_sprites.add(self.player)

		# import other classes
		self.pause_menu = PauseMenu(self.game, self.car_type, self.track)
		self.timer = Timer(self.game)
		self.GUI = GUI(self.game, self)
		self.shadow = Shadow(self.game, self, self.floor_layer, (self.player.rect.x, self.player.rect.y + (2* SCALE)))

	def get_player_start_pos_and_angle(self):
		
		if self.start_orientation['vert'] != 0:
			if not self.reverse_direction:
				if self.start_orientation['vert'] == 1:
					angle = 90
				else:
					angle = -90
				player_pos = [self.start_pos[0] + (self.finish_line.get_width()/2) - (37 * SCALE * 0.5),\
				 self.start_pos[1] + (self.finish_line.get_height()/2) - (37 * SCALE * 0.5) + (150 * self.start_orientation['vert'])]
			else:
				self.start_orientation['vert'] *= -1
				if self.start_orientation['vert'] == 1:
					angle = -90
				else:
					angle = 90
				player_pos = [self.start_pos[0] + (self.finish_line.get_width()/2) - (37 * SCALE * 0.5),\
				 self.start_pos[1] + (self.finish_line.get_height()/2) - (37 * SCALE * 0.5) + (150 * self.start_orientation['vert'])]
			
		if self.start_orientation['hori'] != 0:
			if not self.reverse_direction:
				if self.start_orientation['hori'] == 1:
					angle = 180
				else:
					angle = 0
				player_pos = [self.start_pos[0] + (self.finish_line.get_width()/2) - (37 * SCALE * 0.5) + (150 * self.start_orientation['hori']),\
				 self.start_pos[1] + (self.finish_line.get_height()/2) - (37 * SCALE * 0.5)]
			else:
				self.start_orientation['hori'] *= -1
				if self.start_orientation['hori'] == 1:
					angle = 0
				else:
					angle = 180
				player_pos = [self.start_pos[0] + (self.finish_line.get_width()/2) - (37 * SCALE * 0.5) + (150 * self.start_orientation['hori']),\
				 self.start_pos[1] + (self.finish_line.get_height()/2) - (37 * SCALE * 0.5)]

		return(player_pos, angle)

	def get_track_images(self, path):
		surf = pygame.image.load(f'assets/tracks/{self.track}/{path}.png').convert_alpha()
		surf = pygame.transform.scale(surf, (surf.get_width() * SCALE, surf.get_height() * SCALE))
		mask = pygame.mask.from_surface(surf)
		return (surf, mask)

	def get_checkpoint_images(self):
		for num in self.track_data.keys():
			image = self.track_data[num][0]
			images.append(image)

		if self.reverse_direction:
			images.reverse()

		return image

	def get_checkpoint_positions(self):
		checkpoints = []
		for num in self.track_data.keys():
			img = pygame.image.load(f'assets/tracks/{self.track_data[num][1]}.png')
			img = pygame.transform.scale(img, (img.get_width() * SCALE, img.get_height() * SCALE))
			mask = pygame.mask.from_surface(img)
			checkpoint = self.track_data[num][0]
			checkpoints.append([checkpoint, img, mask])

		if self.reverse_direction:
			checkpoints.reverse()

		return checkpoints

	def collide_checkpoints(self):
		for index, checkpoint in enumerate(self.checkpoints):
			if self.player.collide(checkpoint[2], *checkpoint[0]) != None:
				if index not in self.anti_cheat_reverse_checkpoints:
					self.anti_cheat_reverse_checkpoints.append(index) 
				if any(i == index-1 for i in self.passed_checkpoints) == True:
					if index not in self.passed_checkpoints:
						self.passed_checkpoints.append(index) 

	def collide_finish_line(self):
		if self.player.collide(self.finish_line_mask, *self.start_pos):
			self.anti_cheat_reverse_checkpoints = []

		if self.reverse_direction:
			if self.start_orientation['vert'] == -1 and self.player.hitbox.centery < self.start_pos[1] or\
			self.start_orientation['vert'] == 1 and self.player.hitbox.centery > self.start_pos[1] + self.finish_line.get_height() or\
			self.start_orientation['hori'] == -1 and self.player.hitbox.centerx < self.start_pos[0] or\
			self.start_orientation['hori'] == 1 and self.player.hitbox.centerx > self.start_pos[0] + self.finish_line.get_width():
				if not self.player.collide(self.finish_line_mask, *self.start_pos)\
				and self.anti_cheat_reverse_checkpoints == []:
					if self.passed_checkpoints == [-1]:
						self.started_race = True
					elif list(self.passed_checkpoints)[-1] == self.num_of_checkpoints:
				 		self.passed_checkpoints = [-1]
				 		self.lap_times.append(self.timer.get_elapsed_time())
				 		self.timer.reset()

		else:
			if self.start_orientation['vert'] == 1 and self.player.hitbox.centery < self.start_pos[1] or\
			self.start_orientation['vert'] == -1 and self.player.hitbox.centery > self.start_pos[1] + self.finish_line.get_height() or\
			self.start_orientation['hori'] == 1 and self.player.hitbox.centerx < self.start_pos[0] or\
			self.start_orientation['hori'] == -1 and self.player.hitbox.centerx > self.start_pos[0] + self.finish_line.get_width():
				if not self.player.collide(self.finish_line_mask, *self.start_pos)\
				and self.anti_cheat_reverse_checkpoints == []:
					if self.passed_checkpoints == [-1]:
						self.started_race = True
					elif list(self.passed_checkpoints)[-1] == self.num_of_checkpoints:
				 		self.passed_checkpoints = [-1]
				 		self.lap_times.append(self.timer.get_elapsed_time())
				 		self.timer.reset()
	

	def draw_gui_text(self, surf, text, colour, size, pos):
		text_surf = self.font.render(text, True, colour, size)
		text_rect = text_surf.get_rect(center = pos)
		surf.blit(text_surf, text_rect)


	def create_particles(self):
		keys = pygame.key.get_pressed()
		
		if (self.player.difference < -45 or self.player.difference > 45) or \
		(self.player.speed > 1 and (self.player.speed < 6 and keys[pygame.K_UP])):
			self.dust = Dust(self.game, self, self.floor_layer, (self.player.rect.center))

		if (self.player.difference < -20 or self.player.difference > 20) or \
		(self.player.speed > 1 and (self.player.speed < 6 and keys[pygame.K_UP])):
			self.skidmarks = Skidmarks(self.game, self, self.floor_layer, (self.player.rect.centerx, self.player.rect.centery + (2* SCALE)))

	def toggle_pause(self):
		if ACTIONS['space']:
			self.timer.stopstart()
			new_state = PauseMenu(self.game, self.car_type, self.track)
			new_state.enter_state()
		self.game.reset_keys()

	def update(self):

		self.all_sprites.update()
		self.floor_layer.update()

		if not self.finished_race:
			self.toggle_pause()
			self.player.input()

		self.collide_checkpoints()
		self.collide_finish_line()

		if self.player.collide(self.gravel_trap_mask) != None:
			self.player.speed *= 0.95

	def render(self, display):
		
		display.fill(BLUE)
		self.all_sprites.offset_draw(self.player)

		#self.game.render_text(str(f'{self.game.clock.get_fps(): .1f}'), WHITE, self.game.big_font, (HALF_WIDTH /1.5, HEIGHT * 0.9))
		
		self.GUI.update()

		if self.started_race:
			self.timer.update()

		# fadein and next state
		display.blit(self.fade_surf, self.fade_rect)
		self.fade_surf.set_alpha(self.fadein_alpha)

		self.fadein_alpha -= 255//50
		if self.fadein_alpha <= 0:
			self.fadein_alpha = 0
				


