#! python 3

import math
import pygame
from pprint import pprint

grad = math.pi / 180
def radians_to_degrees(radians):
    return (radians / math.pi) * 180.0
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180.0)

class Ship(pygame.sprite.Sprite):
	id = 1
	collection = {}
	def __init__(self, start = [320, 480], direction = 0):
		self.id = Ship.id
		Ship.id += 1
		Ship.collection[self.id] = self
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.x = start[0]
		self.y = start[1]
		self.dx = 0
		self.dy = 0
		self.direction = direction
		self.angle = degrees_to_radians(direction)
		self.sprite = pygame.image.load('resources/sprites/rifter.png')
		self.image = self.sprite
		self.rect = self.image.get_rect()
		self.speed = 0.0

	def turn(self, change):
		if (change > 0):
			self.direction -= 5
		else:
			self.direction += 5
		if self.direction > 360:
			self.direction -= 360
		if self.direction < 0:
			self.direction += 360
			
		self.angle = degrees_to_radians(self.direction)
		self.dx = math.sin(self.angle)
		self.dy = math.cos(self.angle)

	def accelerate(self):
		self.speed += 0.2
		if self.speed > 4.0:
			self.speed = 4.0

	def deccelerate(self):
		self.speed -= 0.2
		if self.speed < 0.0:
			self.speed = 0

	def update(self):
		if self.speed > 0.0:
			self.x += self.dx * self.speed
			self.y += self.dy * self.speed
			self.speed -= 0.1
		self.image = pygame.transform.rotate(self.sprite, self.direction - 180)
		self.rect = self.image.get_rect()
		self.rect.centerx = self.x
		self.rect.centery = self.y

pygame.init()
display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screenInfo = pygame.display.Info()
screenWidth, screenHeight = screenInfo.current_w / 2, screenInfo.current_h / 2
screen = pygame.Surface((screenWidth, screenHeight))
clock = pygame.time.Clock()
fps = 60
playtime = 0.0 # seconds

rifterProjectiles = []

keys = [False, False, False, False, False] # up, down, left, right, space

shipGroup = pygame.sprite.Group()
everythingGroup = pygame.sprite.LayeredUpdates()
Ship.groups = shipGroup, everythingGroup

player = Ship([320, 240], 0)

gameloop = True
while gameloop:
	ms = clock.tick(fps)
	playtime += ms / 1000.0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameloop = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				keys[0] = True
			if event.key == pygame.K_s:
				keys[1] = True
			if event.key == pygame.K_a:
				keys[2] = True
			if event.key == pygame.K_d:
				keys[3] = True
			if event.key == pygame.K_SPACE:
				keys[4] = True
			if event.key == pygame.K_ESCAPE:
				gameloop = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				keys[0] = False
			if event.key == pygame.K_s:
				keys[1] = False
			if event.key == pygame.K_a:
				keys[2] = False
			if event.key == pygame.K_d:
				keys[3] = False
			if event.key == pygame.K_SPACE:
				keys[4] = False
			
	if keys[0]: # w
		player.accelerate()
	elif keys[1]: # s
		player.deccelerate()
	if keys[2]: # a
		player.turn(-1)
	elif keys[3]: # d
		player.turn(1)
	if keys[4]:
		projectile = (player.x, player.y, math.sin(player.angle), math.cos(player.angle))
		rifterProjectiles.append(projectile)
		keys[4] = False;

	for i in range(len(rifterProjectiles)):
		projectile = rifterProjectiles[i]
		p_X, p_Y, p_XN, p_YN = rifterProjectiles[i][0], rifterProjectiles[i][1], rifterProjectiles[i][2], rifterProjectiles[i][3] # current and next X,Y
		p_X += p_XN * 10
		p_Y += p_YN * 10
		rifterProjectiles[i] = (p_X, p_Y, p_XN, p_YN)

	for projectile in rifterProjectiles:
		if projectile[0] < 0 or projectile[1] < 0 or projectile[0] > screenWidth or projectile[1] > screenHeight:
			rifterProjectiles.remove(projectile)

	for projectile in rifterProjectiles:
		pygame.draw.rect(screen, (255,255,255), [int(projectile[0]) - 1, int(projectile[1]) - 1, 3, 3])

	everythingGroup.clear(screen, display)
	everythingGroup.update()
	everythingGroup.draw(screen)

	pygame.transform.scale2x(screen, display)
	pygame.display.update()
	
pygame.quit()
exit(0)