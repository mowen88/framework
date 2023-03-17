from settings import *

class Cache:
	def __init__(self):
		self.sprite_cache = {}
		self.angle = 360 // ANGLE_COUNT
		self.get_sprite_cache()

	def get_sprite_cache(self):
		for name in CAR_DATA:
			self.sprite_cache[name] = {'rotated_sprites':{}}

			data = CAR_DATA[name]
			layer_images = self.get_layer_images(data)
			self.prerender(name, layer_images, data)

	def prerender(self, name, layer_images, data):
		for angle in range(ANGLE_COUNT):
			surf = pygame.Surface(layer_images[0].get_size())
			surf = pygame.transform.rotate(surf, angle)
			sprite_surf = pygame.Surface((150, 150), pygame.SRCALPHA)

			offset = 0
			for index, layer in enumerate(layer_images):
				offset += 2
				layer = pygame.transform.rotate(layer, self.angle)
				sprite_surf.blit(layer, ((75 - layer.get_width() /2), index + offset + (75 - layer.get_height() / 2)))
				
			outline_coordinates = pygame.mask.from_surface(sprite_surf).outline()
			pygame.draw.polygon(sprite_surf, BLACK, outline_coordinates, width=SCALE)
			
			image = pygame.transform.flip(sprite_surf, True, True)
			self.sprite_cache[name]['rotated_sprites'][angle] = image

	def get_layer_images(self, data):
		spritesheet = pygame.image.load(data['path']).convert_alpha()
		spritesheet = pygame.transform.scale(spritesheet, (spritesheet.get_width() * SCALE, spritesheet.get_height() * SCALE))
		sheet_w = spritesheet.get_width()
		sheet_h = spritesheet.get_height()

		spritesheet = pygame.transform.scale(spritesheet, (sheet_w, sheet_h))
		sprite_h = sheet_h // data['layer_count']
		sheet_h = sprite_h * data['layer_count']

		layer_images = []
		for y in range(0, sheet_h, sprite_h):
			sprite = spritesheet.subsurface((0, y, sheet_w, sprite_h))
			layer_images.append(sprite)
		return layer_images[::-1]
