import sys, pygame, csv
from pygame import mixer
from operator import itemgetter
from os import walk
from settings import *
from title import Title
from level import Level
from leaderboard import Leaderboard 

class Game():
	def __init__(self):

		pygame.init()

		#sound
		mixer.init()

		self.accel_fx = pygame.mixer.Sound('audio/accel.wav')
		self.decel_fx = pygame.mixer.Sound('audio/decel.wav') 

		self.accel_fx.set_volume(0.1)
		self.decel_fx.set_volume(0.1)

		self.clock = pygame.time.Clock()
		# self.time = 0
		# self.dt = 0.1

		#self.screen = pygame.display.set_mode((RES), pygame.FULLSCREEN|pygame.SCALED)
		self.screen = pygame.display.set_mode((RES))

		self.running = True
		self.playing = True
 
		self.stack = []

		#font
		self.small_font = pygame.font.Font(FONT, 30)
		self.bigger_font = pygame.font.Font(FONT, 42)
		self.smaller_font = pygame.font.Font(FONT, 18)
		self.even_smaller_font = pygame.font.Font(FONT, 12)
		self.big_font = pygame.font.Font(FONT, 24)

		self.get_leaderboard()
		# print(LEADERBOARD_DATA)

		self.player_name = ''
		self.name_entry_active = False
		self.track = list(TRACK_DATA.keys())[0]
		self.fastest_lap = None
		self.total_laps = 1
		self.reverse_direction = True
		self.car_type = list(CAR_DATA.keys())[0]

		self.load_states() 

	def create_level(self, car, track):
		Level(self, car, track).enter_state()

	def get_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					ACTIONS['escape'] = True
					self.running = False
					self.playing = False

				elif event.key == pygame.K_UP:
					ACTIONS['up'] = True
				elif event.key == pygame.K_DOWN:
					ACTIONS['down'] = True
				elif event.key == pygame.K_RIGHT:
					ACTIONS['right'] = True
				elif event.key == pygame.K_LEFT:
					ACTIONS['left'] = True
				elif event.key == pygame.K_SPACE:
					ACTIONS['space'] = True
				elif event.key == pygame.K_RETURN:
					ACTIONS['return'] = True
				elif event.key == pygame.K_BACKSPACE:
					ACTIONS['backspace'] = True

				if self.name_entry_active:
					if event.key == pygame.K_BACKSPACE:
						self.player_name = self.player_name[:-1]

					elif len(self.player_name) < 10:
						self.player_name += event.unicode

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					ACTIONS['up'] = False
				elif event.key == pygame.K_DOWN:
					ACTIONS['down'] = False
				if event.key == pygame.K_RIGHT:
					ACTIONS['right'] = False
				elif event.key == pygame.K_LEFT:
					ACTIONS['left'] = False
				elif event.key == pygame.K_SPACE:
					ACTIONS['space'] = False

			if event.type == pygame.MOUSEWHEEL:
				if event.y == 1:
					ACTIONS['scroll_up'] = True
				elif event.y == -1:
					ACTIONS['scroll_down'] = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					ACTIONS['left_click'] = True
				elif event.button == 3:
					ACTIONS['right_click'] = True
				elif event.button == 4:
					ACTIONS['scroll_down'] = True
				elif event.button == 2:
					ACTIONS['scroll_up'] = True

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					ACTIONS['left_click'] = False
				elif event.button == 3:
					ACTIONS['right_click'] = False
				elif event.button == 4:
					ACTIONS['scroll_down'] = False
				elif event.button == 2:
					ACTIONS['scroll_up'] = False

	def reset_keys(self):
		for key_pressed in ACTIONS:
			ACTIONS[key_pressed] = False

	def update(self):
		#pygame.display.set_caption(str(self.clock.get_fps()))
		#self.dt = self.clock.tick()
		self.stack[-1].update()

	def render(self):
		self.stack[-1].render(self.screen)
		pygame.display.flip()

	def get_time(self):
		self.time = pygame.time.get_ticks() / 1000

	def load_states(self):
		self.title_screen = Title(self)
		self.stack.append(self.title_screen)

	def import_folder(self, path):
		surf_list = []

		for _, __, img_files in walk(path):
			for img in img_files:
				full_path = path + '/' + img
				img_surf = pygame.image.load(full_path).convert_alpha()
				img_surf = pygame.transform.scale(img_surf,(img_surf.get_width() * SCALE, img_surf.get_height() * SCALE))
				surf_list.append(img_surf)

		return surf_list

	def get_image(self, path, size, pos):
		surf = pygame.image.load(path).convert_alpha()
		surf = pygame.transform.scale(surf, size)
		rect = surf.get_rect(center = pos)
		return(surf, rect)

	def render_text(self, text, colour, font, pos):
		surf = font.render(str(text), True, colour)
		rect = surf.get_rect(center = pos)
		self.screen.blit(surf, rect)

	def get_leaderboard(self):
		with open('leaderboard.csv', mode ='r') as leaderboard_file:
			leaderboard = csv.reader(leaderboard_file)
			for index, row in enumerate(leaderboard):
				if row:
					LEADERBOARD_DATA.append(row)

	def run(self):
		self.clock.tick(FPS)
		self.get_events()
		#self.get_time()
		self.update()
		self.render()

if __name__ == "__main__":
	g = Game()
	while g.running:
		g.run()