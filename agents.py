import pygame
import random as r
import numpy
import time
import math
import sys

"""
Global constants
"""
# Colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
BLUE = ( 0, 0, 255)
RED = ( 255, 0, 0)
ORANGE = ( 255, 127, 0)
GREEN = ( 0, 255, 0)
OTHER = ( 0, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
agent_size = 8.0
be = 1.65
iterations = 600

tick = 60
is_print_map = False
use_int4 = False

class Player(pygame.sprite.Sprite):
	""" This class represents the bar at the bottom that the player controls. """
	
	cooperate = False
	score = 0.0
	x = 0
	y = 0
	n_cop = False
	n_sc = 0.0
	
	# Constructor function
	def __init__(self, x, y, size = 1):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([size, size])
		
		if r.random() <= 1:
			self.cooperate = True
		
		if self.cooperate:
			self.image.fill(WHITE)
		else:
			self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.x = x*size
		self.rect.y = y*size
		self.x = x
		self.y = y
	
	def interact_4(self):
		self.score = 0.0
		if self.x > 0:
			self.score += self.comp_score(mapa[self.x - 1][self.y])
		if self.y > 0:
			self.score += self.comp_score(mapa[self.x][self.y - 1])
		if self.x < matrix_lines - 1:
			self.score += self.comp_score(mapa[self.x + 1][self.y])
		if self.y < matrix_cols - 1:
			self.score += self.comp_score(mapa[self.x][self.y + 1])
			
	def interact_8(self):
		self.score = 0.0
		if self.x > 0:
			self.score += self.comp_score(mapa[self.x - 1][self.y])
			if self.y > 0:
				self.score += self.comp_score(mapa[self.x - 1][self.y - 1])
			if self.y < matrix_cols - 1:
				self.score += self.comp_score(mapa[self.x - 1][self.y + 1])
		if self.x < matrix_lines - 1:
			self.score += self.comp_score(mapa[self.x + 1][self.y])
			if self.y > 0:
				self.score += self.comp_score(mapa[self.x + 1][self.y - 1])
			if self.y < matrix_cols - 1:
				self.score += self.comp_score(mapa[self.x + 1][self.y + 1])
		if self.y > 0:
			self.score += self.comp_score(mapa[self.x][self.y - 1])
		if self.y < matrix_cols - 1:
			self.score += self.comp_score(mapa[self.x][self.y + 1])
	
	def update_8(self):
		ini_x = self.x
		fin_x = self.x
		ini_y = self.y
		fin_y = self.y
		
		if self.x > 0:
			ini_x = self.x-1
		if self.x < matrix_lines-1:
			fin_x = self.x+1
		if self.y > 0:
			ini_y = self.y-1
		if self.y < matrix_cols-1:
			fin_y = self.y+1
		best = self.score
		change = None
		for i in range(ini_x,fin_x+1):
			for j in range(ini_y,fin_y+1):
				if(i != self.x or j != self.y):
					ag = mapa[i][j]
					if best < ag.score:
						best = ag.score
						change = ag.cooperate
					elif best == ag.score:
						if not ag.cooperate:
							change = ag.cooperate
		return (best,change)
		
	def update_4(self):
		best = self.score
		change = None
		if self.x > 0:
			ag = mapa[self.x - 1][self.y]
			if best < ag.score:
				best = ag.score
			change = ag.cooperate
		if self.y > 0:
			ag = mapa[self.x][self.y - 1]
			if best < ag.score:
				best = ag.score
				change = ag.cooperate
		if self.x < matrix_lines - 1:
			ag = mapa[self.x + 1][self.y]
			if best < ag.score:
				best = ag.score
				change = ag.cooperate
		if self.y < matrix_cols - 1:
			ag = mapa[self.x][self.y + 1]
			if best < ag.score:
				best = ag.score
				change = ag.cooperate
		return (best,change)
	
	def update(self):
		best = self.score
		change = None
		if use_int4:
			best, change = self.update_4()
		else:	
			best, change = self.update_8()
		if change != None and self.cooperate != change:
			if self.cooperate and not change:
				self.image.fill(ORANGE)
			elif not self.cooperate and change:
				self.image.fill(GREEN)
			#self.n_cop = change
			self.n_cop = change
		else:
			if self.cooperate:
				self.image.fill(WHITE)
			else:
				self.image.fill(RED)
			self.n_cop = self.cooperate
	
	def comp_score(self, p):
		if self.cooperate and p.cooperate:
			return 1
		elif self.cooperate and (not p.cooperate):
			return 0
		elif not self.cooperate and not p.cooperate:
			return 0
		else:
			return be
	
	def next_gen(self):
		self.cooperate = self.n_cop
		self.score = 0.0

def print_map():
	for j in range(matrix_lines):
		s = ""
		for i in range(matrix_cols):
			if mapa[i][j].cooperate:
				s += "(" + str(mapa[i][j].score) + ") "
			else:
				s += "[" + str(mapa[i][j].score) + "] "
		print s
	print "\n"

matrix_lines =  int(SCREEN_HEIGHT/agent_size)
matrix_cols =  int(SCREEN_WIDTH/agent_size)

pygame.init()
screen = pygame.display.set_mode([SCREEN_HEIGHT,SCREEN_WIDTH])

pygame.display.set_caption('Test')
all_sprite_list = pygame.sprite.Group()

mapa = []

for i in range(matrix_lines):
	temp = []
	for j in range(matrix_cols):
		p = Player(i, j, agent_size)
		#mapa[i][j] = p
		temp.append(p)
		all_sprite_list.add(p)
	mapa.append(temp)

clock = pygame.time.Clock()
done = False

mapa[matrix_lines/2-1][matrix_cols/2-1].cooperate = False

initial_time = time.time()
it = 0
while not done:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		#elif event.type == pygame.KEYDOWN:
		#	if event.key == pygame.K_LEFT:

	if it <= iterations:
		all_sprite_list.update()
		
		screen.fill(BLACK)
		
		all_sprite_list.draw(screen)
		
		pygame.display.flip()
		
		clock.tick(tick)

		for i in range(matrix_lines):
			for j in range(matrix_cols):
				if use_int4:
					mapa[i][j].interact_4()
				else:
					mapa[i][j].interact_8()
				if i > 1:
					mapa[i-2][j].update()

		for i in range(matrix_lines - 2,matrix_lines):
			for j in range(matrix_cols):
				mapa[i][j].update()
		
		for i in range(matrix_lines):
			for j in range(matrix_cols):
				mapa[i][j].next_gen()
		it += 1
