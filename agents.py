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

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
agent_size = 5.0
be = 1.4
tick = 10
is_print_map = True

class Player(pygame.sprite.Sprite):
	""" This class represents the bar at the bottom that the player controls. """
	
	cooperate = False
	score = 0.0
	x = 0
	y = 0
	
	# Constructor function
	def __init__(self, x, y, size = 1):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([size, size])
		
		if r.random() <= 0.5:
			self.cooperate = True
		
		if self.cooperate:
			self.image.fill(WHITE)
		else:
			self.image.fill(RED)
		
		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.x = x*size
		self.rect.y = y*size
		self.x = x
		self.y = y
	
	def interact(self):
		self.score = 0
		if self.x > 0:
			self.score += self.comp_score(mapa[self.x - 1][self.y])
		if self.y > 0:
			self.score += self.comp_score(mapa[self.x][self.y - 1])
		if self.x < matrix_lines - 1:
			self.score += self.comp_score(mapa[self.x + 1][self.y])
		if self.y < matrix_cols - 1:
			self.score += self.comp_score(mapa[self.x][self.y + 1])
	
	def update(self):
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
		if change != None and self.cooperate != change:
			if self.cooperate and not change:
				self.image.fill(ORANGE)
			elif not self.cooperate and change:
				self.image.fill(GREEN)
			self.cooperate = change
		else:
			if self.cooperate:
				self.image.fill(WHITE)
			else:
				self.image.fill(RED)
	
	def comp_score(self, p):
		if self.cooperate and p.cooperate:
			return 1
		elif self.cooperate and (not p.cooperate):
			return 0
		elif not self.cooperate and not p.cooperate:
			return 0
		else:
			return be

def print_map():
	for i in range(matrix_lines):
		s = ""
		for j in range(matrix_cols):
			s += str(mapa[i][j].score) + " "
		print s
	print "\n"

matrix_lines =  int(SCREEN_HEIGHT/agent_size)
matrix_cols =  int(SCREEN_WIDTH/agent_size)
# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_HEIGHT,SCREEN_WIDTH])

# Set the title of the window
pygame.display.set_caption('Test')

# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()

#mapa = [[ for x in xrange(SCREEN_WIDTH)] for x in xrange(SCREEN_HEIGHT)] 
#mapa = numpy.zeros((SCREEN_WIDTH, SCREEN_HEIGHT))
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


initial_time = time.time()
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	all_sprite_list.update()
	
	screen.fill(BLACK)
	
	all_sprite_list.draw(screen)
	
	pygame.display.flip()
	
	clock.tick(tick)
	
	for i in range(matrix_lines):
		for j in range(matrix_cols):
			mapa[i][j].interact()
			if i > 1:
				mapa[i-2][j].update()
				
	for i in range(matrix_lines - 2,matrix_lines):
		for j in range(matrix_cols):
			mapa[i][j].update()
	
	if is_print_map:
		print_map()
		
	
	#0 1 2 3 4 5 6 7 8 9
#	for j in range(matrix_lines):
#		for i in range(matrix_cols):
#			mapa[i][j].update()

