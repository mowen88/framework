from settings import *
import math

class StackedSprite(pygame.sprite.Sprite):
	def __init__(self, game, level, name, pos, start_angle):
		super().__init__()

		self.game = game
		self.level = level
		self.name = name
		self.angle = start_angle

		self.surf_size = (37 * SCALE, 37 * SCALE)
		self.image = pygame.Surface(self.surf_size)
		self.pos = pygame.math.Vector2(pos)
		self.rect = self.image.get_rect(center = self.pos)
		self.hitbox = self.rect.inflate(0, 0)
		
		self.data = CAR_DATA[self.name]

		self.layer_images = self.get_layer_images()

		self.grip = self.data['grip']
		self.acc = self.data['acc'] * self.level.friction
		self.braking = self.data['braking'] * self.level.friction
		self.max_speed = self.data['max_speed']
		self.speed = 0
		self.friction = self.level.friction + self.grip
		self.momentum_direction = 0
		self.steer_speed = 0
		self.slip_angle = 5 * self.friction
		self.difference = 0

	def get_layer_images(self):
		spritesheet = pygame.image.load(f'assets/stacked_sprites/{self.name}.png').convert_alpha()
		spritesheet = pygame.transform.scale(spritesheet, (spritesheet.get_width() * SCALE, spritesheet.get_height() * SCALE))
		sheet_w = spritesheet.get_width()
		sheet_h = spritesheet.get_height()

		spritesheet = pygame.transform.scale(spritesheet, (sheet_w, sheet_h))
		sprite_h = sheet_h // self.data['layer_count']
		sheet_h = sprite_h * self.data['layer_count']

		layer_array = []
		for y in range(0, sheet_h, sprite_h):
			sprite = spritesheet.subsurface((0, y, sheet_w, sprite_h))
			layer_array.append(sprite)
		return layer_array[::-1]

	def get_image(self):
		surf = pygame.Surface(self.layer_images[0].get_size())
		sprite_surf = pygame.Surface(self.surf_size, pygame.SRCALPHA)

		for index, layer in enumerate(self.layer_images):
			layer = pygame.transform.rotate(layer, self.angle)
			sprite_surf.blit(layer, ((75 - layer.get_width() /2), (index * 2) + (75 - layer.get_height() / 2)))
			
		outline_coordinates = pygame.mask.from_surface(sprite_surf).outline()
		pygame.draw.polygon(sprite_surf, BLACK, outline_coordinates, width=SCALE)
		
		self.image = pygame.transform.flip(sprite_surf, True, True)

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP]:
			if self.speed > 0:
				self.speed = min(self.speed + self.acc, self.max_speed)

			else:
				self.speed = min(self.speed + self.braking, self.max_speed)

		elif keys[pygame.K_DOWN]:
			if self.speed > 0:
				self.speed = max(self.speed - self.braking, -2)
			else:
				self.speed = max(self.speed - self.acc, -2)
		
		else:
			if self.speed > 0:
				self.speed = max(self.speed - 0.1, 0)
			elif self.speed < 0:
				self.speed = min(self.speed + self.braking, 0)

		if self.speed >= 0:
			self.difference = self.momentum_direction - self.angle

			if keys[pygame.K_LEFT]:
				self.steer_speed += self.speed / self.slip_angle
			
			if keys[pygame.K_RIGHT]:
				self.steer_speed -= self.speed / self.slip_angle
			
			if self.difference > 0:
				self.momentum_direction -= self.slip_angle
				self.speed -= (self.difference/50)*self.friction

			elif self.difference < 0:
				self.momentum_direction += self.slip_angle
				self.speed += (self.difference/50)*self.friction

		else:
			self.momentum_direction = self.angle

			if keys[pygame.K_LEFT]:
				self.steer_speed += self.speed / self.slip_angle 
			
			if keys[pygame.K_RIGHT]:
				self.steer_speed -= self.speed / self.slip_angle

	def move(self):
		vertical = math.sin(math.radians(self.momentum_direction)) * self.speed
		horizontal = math.cos(math.radians(self.momentum_direction)) * self.speed
		self.pos.x += horizontal
		self.pos.y -= vertical

		self.steer_speed *= 0.4

		self.angle += self.steer_speed

		self.hitbox.x = self.pos.x
		self.hitbox.y = self.pos.y
		self.rect.center = self.hitbox.center

	def collide(self, mask, x=0, y=0):
		car_mask = pygame.mask.from_surface(self.image)
		offset = (int(self.pos.x - x),int(self.pos.y - y))
		intersect_point = mask.overlap(car_mask, offset)
		return intersect_point

	def bump(self):
		self.speed = - self.speed

	def update(self):
		self.move()
		self.get_image()
		self.level.create_particles()

		



# class Entity(pygame.sprite.Sprite):
# 	def __init__(self, game, level, name, pos):
# 		super().__init__()

# 		self.game = game
# 		self.level = level
# 		self.name = name
# 		self.pos = pygame.math.Vector2(pos)
# 		self.image_type = pygame.image.load(f'assets/{self.name}.png').convert_alpha()
# 		self.image_type = pygame.transform.scale(self.image_type, (self.image_type.get_width() * SCALE, self.image_type.get_height() * SCALE))
# 		self.image = self.image_type
# 		self.direction = pygame.math.Vector2(pos)
# 		self.rect = self.image.get_rect(center = self.direction)
# 		self.hitbox = self.rect.inflate(0, 0)

# 		self.data = CAR_DATA[self.name]
		
# 		self.grip = self.data['grip']
# 		self.acc = self.data['acc'] * self.level.friction
# 		self.braking = self.data['braking'] * self.level.friction
# 		self.max_speed = self.data['max_speed']
# 		self.speed = 0
# 		self.friction = self.level.friction + self.grip
# 		self.momentum_direction = 0
# 		self.angle = 0
# 		self.steer_speed = 0
# 		self.slip_angle = 5 * self.friction

# 	def input(self):
# 		keys = pygame.key.get_pressed()
# 		if keys[pygame.K_UP]:
# 			self.speed = min(self.speed + self.acc, self.max_speed)

# 		else:
# 			self.speed = max(self.speed - self.braking, 0)

# 		if self.speed > 0:
# 			difference = self.momentum_direction - self.angle
# 			if keys[pygame.K_LEFT]:
# 				self.steer_speed += self.speed / self.slip_angle

# 			if keys[pygame.K_RIGHT]:
# 				self.steer_speed -= self.speed / self.slip_angle
			
# 			if difference > 0:
# 				self.momentum_direction -= self.slip_angle
# 			elif difference < 0:
# 				self.momentum_direction += self.slip_angle

# 		else:
# 			self.momentum_direction = self.angle


# 	def move(self):
# 		vertical = math.cos(math.radians(self.momentum_direction)) * self.speed
# 		horizontal = math.sin(math.radians(self.momentum_direction)) * self.speed
# 		self.direction.x -= horizontal
# 		self.direction.y -= vertical

# 	def rotate_sprite(self):
# 		self.image = pygame.transform.rotate(self.image_type, self.angle)
# 		self.rect = self.image.get_rect(center = self.rect.center)

# 		self.hitbox.x = self.direction.x
# 		self.hitbox.y = self.direction.y
# 		self.rect.center = self.hitbox.center

# 	def update(self):
# 		self.input()
# 		self.move()
# 		self.rotate_sprite()
# 		self.steer_speed *= 0.75
# 		self.angle += self.steer_speed
		

		
		