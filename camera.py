import pygame, csv, random, math
from settings import *

class Camera(pygame.sprite.Group):
	def __init__(self, game, level):
		super().__init__()
		self.game = game
		self.level = level
		self.offset = pygame.math.Vector2()
		

	def offset_draw(self, target):

		#self.game.screen.blit(self.level.bg,(0 - target.rect.centerx, 0 - self.offset[1]))
		self.game.screen.blit(self.level.track_img,(0 - self.offset[0], 0 - self.offset[1]))
		self.game.screen.blit(self.level.finish_line,(self.level.start_pos[0] - self.offset[0], self.level.start_pos[1] - self.offset[1]))
		
		self.offset[0] += (target.rect.centerx - self.offset[0] - HALF_WIDTH)
		self.offset[1] += (target.rect.centery - self.offset[1] - HALF_HEIGHT)

		for sprite in self.level.floor_layer:
			offset = sprite.rect.topleft - self.offset
			self.game.screen.blit(sprite.image, offset)

		for sprite in self.level.all_sprites:
			offset = sprite.rect.topleft - self.offset
			self.game.screen.blit(sprite.image, offset)

		
