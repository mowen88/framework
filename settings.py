import pygame

# screen
RES = WIDTH, HEIGHT = pygame.math.Vector2(1280, 720)
HALF_WIDTH, HALF_HEIGHT = RES / 2
#HALF_HEIGHT = RES[1] / 2
#CENTRE = HALF_WIDTH, HALF_HEIGHT = RES // 2

FPS = 60
SCALE = 4

# game fonts
FONT = 'font/Pokemon Classic.ttf'
FONT_2 = 'font/minimal/Minimal.ttf'

# game colours
BLACK = ((9, 9, 14))
GREY = ((91,83,145))
LIGHT_GREY = ((146, 143, 184))
WHITE = ((255, 255, 255)) 
BLUE = ((20, 68, 145))
LIGHT_BLUE = ((113, 181, 219))
RED = ((112, 21, 31))
ORANGE = ((227, 133, 36))
PINK = ((195, 67, 92))
GREEN = ((88, 179, 150))
LIGHT_GREEN = ((106, 226, 145))
PURPLE = ((66, 0, 78))
CYAN = ((0, 255, 255))
MAGENTA = ((153, 60, 139))
YELLOW = ((224, 225, 146))

# key events
ACTIONS = {'escape': True, 'space': False, 'up': False, 'down': False, 'left': False, 'right': False, 'return': False, 'left_click': False, 'right_click': False, 'scroll_up': False, 'scroll_down': False}

ATTRIBUTES = {
	'car':{'path':'assets/stacked_sprites/car.png',
	'layer_count': 9,
	'scale': 3}
}

# car specs
CAR_DATA = {
	'i-type':{'acc': 1.4, 'braking':1.4, 'max_speed': 18, 'grip': 0.175, 'layer_count': 8},
	'i-pace':{'acc': 1.4, 'braking':1.4, 'max_speed': 15, 'grip': 0.1, 'layer_count': 10},
	'xjr13':{'acc': 1.4, 'braking':1.4, 'max_speed': 18, 'grip': 0.1, 'layer_count': 8}
	
}

LEADERBOARD_DATA = []

# car specs
TRACK_DATA = {
	'Small Track':{'checkpoints':{
				   0:[[15.5*16*SCALE, 20*16*SCALE],'hori_checkpoint'],
				   1:[[34*16*SCALE, 2.5*16*SCALE],'vert_checkpoint'],
				   2:[[45.5*16*SCALE, 12.5*16*SCALE], 'vert_checkpoint'],
				   3:[[54.5*16*SCALE, 2.5*16*SCALE], 'vert_checkpoint'],
				   4:[[53.5*16*SCALE, 13.5*16*SCALE], 'hori_checkpoint'],
				   5:[[53.5*16*SCALE, 21.5*16*SCALE], 'hori_checkpoint'],
				   6:[[52.5*16*SCALE, 21.5*16*SCALE], 'vert_checkpoint'],
				   7:[[42.5*16*SCALE, 21.5*16*SCALE], 'vert_checkpoint'],
				   8:[[23.5*16*SCALE, 32.5*16*SCALE], 'vert_checkpoint'],
				   9:[[13.5*16*SCALE, 31.5*16*SCALE], 'hori_checkpoint']
			   },
			   'start_pos': [16.5*16*SCALE, 24*16*SCALE],
			   'start_orientation': {'vert': 1, 'hori': 0},
			   'fastest_lap':{
				   'car': '???',
				   'weather':'???',
				   'name': '???'
			   }
			   },
    'Big Track':{'checkpoints':{
				   0:[[55.5*16*SCALE, 22.5*16*SCALE],'vert_checkpoint'],
				   1:[[45.5*16*SCALE, 41.5*16*SCALE],'hori_checkpoint'],
				   2:[[35.5*16*SCALE, 41.5*16*SCALE],'hori_checkpoint'],
				   3:[[34.5*16*SCALE, 22.5*16*SCALE],'vert_checkpoint'],
				   4:[[15.5*16*SCALE, 20.5*16*SCALE],'hori_checkpoint'],
				   5:[[33.5*16*SCALE, 2.5*16*SCALE],'vert_checkpoint'],
				   6:[[45*16*SCALE, 12.5*16*SCALE],'vert_checkpoint'],
				   7:[[56.5*16*SCALE, 2.5*16*SCALE],'vert_checkpoint'],
				   8:[[71.5*16*SCALE, 2.5*16*SCALE],'vert_checkpoint'],
				   9:[[91.5*16*SCALE, 2.5*16*SCALE],'vert_checkpoint'],
				   10:[[91.5*16*SCALE, 12.5*16*SCALE],'vert_checkpoint'],
				   11:[[81.5*16*SCALE, 22.5*16*SCALE],'vert_checkpoint'],
				  
			   },
			   'start_pos': [66.5*16*SCALE, 23.5*16*SCALE],
			   'start_orientation': {'vert':0, 'hori': 1},
			   'fastest_lap':{
				   'car': '???',
				   'weather':'???',
				   'name': '???'
			   }
			   }

}