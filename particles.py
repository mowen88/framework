import pygame, math
from settings import *

class Shadow(pygame.sprite.Sprite):
	def __init__(self, game, level, groups, pos):
		super().__init__(groups)

		#self.sprite_type = sprite_type
		self.game = game
		self.level = level
		self.original_image = pygame.image.load(f'assets/particles/shadows/{self.level.car_type}.png').convert_alpha()
		self.image = self.original_image.copy()
		self.original_image = pygame.transform.scale(self.original_image, (self.image.get_width() * SCALE, self.image.get_height() * SCALE))
		self.rect = self.image.get_rect(center = pos)
		self.alpha = 100

	def update(self):
		self.image = pygame.transform.rotate(self.original_image, self.level.player.angle)
		self.rect = self.image.get_rect(center = self.rect.center)
		
		self.image = pygame.transform.flip(self.image, True, True)
		
		self.image.set_alpha(self.alpha)

		self.rect.center = (self.level.player.rect.centerx, self.level.player.rect.centery + SCALE)

class Skidmarks(pygame.sprite.Sprite):
	def __init__(self, game, level, groups, pos):
		super().__init__(groups)

		#self.sprite_type = sprite_type
		self.game = game
		self.level = level
		self.original_image = pygame.image.load(f'assets/particles/skidmarks.png').convert_alpha()
		self.image = self.original_image.copy()
		self.original_image = pygame.transform.scale(self.original_image, (self.image.get_width() * SCALE, self.image.get_height() * SCALE))
		self.rect = self.image.get_rect(center = pos)
		self.image = pygame.transform.rotate(self.original_image, self.level.player.momentum_direction)
		self.rect = self.image.get_rect(center = self.rect.center)
		self.image = pygame.transform.flip(self.image, True, True)
		self.alpha = 150

	def update(self):
		self.alpha -= 1
		self.image.set_alpha(self.alpha)
		if self.alpha <= 0:
			self.kill()

class Dust(pygame.sprite.Sprite):
	def __init__(self, game, level, groups, pos):
		super().__init__(groups)

		self.game = game
		self.level = level
		self.frames = self.game.import_folder(f'assets/particles/dust')
		self.frame_index = 0
		self.frame_rate = 0.3
		self.original_image = self.frames[self.frame_index]
		self.image = self.original_image.copy()

		self.rect = self.image.get_rect(center = (pos))
		self.image = pygame.transform.rotate(self.original_image, self.level.player.angle)
		self.rect = self.image.get_rect(center = self.rect.center)
		self.image = pygame.transform.flip(self.image, True, True)

		self.alpha = 50

	def animate(self):
		self.frame_index += self.frame_rate
		if self.frame_index >= len(self.frames) -1:
			self.kill()
		self.image = self.frames[int(self.frame_index)]

	def update(self):
		self.animate()

		self.alpha -= 0.2
		self.image.set_alpha(self.alpha)
		if self.alpha <= 0:
			self.kill()


		

		






