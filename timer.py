import pygame
from settings import *

class Timer:
	def __init__(self, game):
		self.game = game

		self.millisecs = 0
		self.secs = 0
		self.mins = 0
		self.hours = 0

	def get_elapsed_time(self):
	    return "%02d:%02d:%03d" % (self.mins, self.secs, self.millisecs)

	def reset(self):
		self.secs = 0
		self.mins = 0

	def update(self):
		self.millisecs += 1/0.06
		if self.millisecs >= 1000:
			self.secs += 1
			self.millisecs = 0
		if self.secs >= 60:
			self.mins += 1
			self.secs = 0
			



	