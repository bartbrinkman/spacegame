#! python 3

import math
import pygame
from pprint import pprint

grad = math.pi / 180
def radians_to_degrees(radians):
    return (radians / math.pi) * 180.0
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180.0)

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screenInfo = pygame.display.Info()
screenWidth, screenHeight = screenInfo.current_w / 2, screenInfo.current_h / 2
surface = pygame.Surface((screenWidth, screenHeight))
clock = pygame.time.Clock()
fps = 60
playtime = 0.0 # seconds

rifterSprite = pygame.image.load('resources/sprites/rifter.png')
rifterPosition = [320,240]
rifterDirection = 0
rifterAngle = 0
rifterNextPosition = [0.0,0.0]
rifterRotated = True
rifterSpeed = 0.0
rifterProjectiles = []

keys = [False, False, False, False, False] # up, down, left, right, space

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
		rifterSpeed += 0.2 
	elif keys[1]: # s
		rifterSpeed -= 0.2
	if keys[2]: # a
		rifterDirection += 5
		rifterRotated = True
	elif keys[3]: # d
		rifterDirection -= 5
		rifterRotated = True
	if keys[4]:
		projectile = (rifterPosition[0], rifterPosition[1], math.sin(rifterAngle), math.cos(rifterAngle))
		rifterProjectiles.append(projectile)
		keys[4] = False;

	if rifterSpeed > 4.0:
		rifterSpeed = 4.0
	if rifterSpeed > 0.0:
		rifterPosition[0] += rifterNextPosition[0] * rifterSpeed
		rifterPosition[1] += rifterNextPosition[1] * rifterSpeed
		rifterSpeed -= 0.1
	if rifterSpeed < 0.0:
		rifterSpeed = 0

	if rifterRotated:
		rifterRotated = False
		if rifterDirection > 360:
			rifterDirection = 0
		if rifterDirection < 0:
			rifterDirection = 359
		rifterAngle = degrees_to_radians(rifterDirection)
		rifterNextPosition[0] = math.sin(rifterAngle)
		rifterNextPosition[1] = math.cos(rifterAngle)

	for i in range(len(rifterProjectiles)):
		projectile = rifterProjectiles[i]
		p_X, p_Y, p_XN, p_YN = rifterProjectiles[i][0], rifterProjectiles[i][1], rifterProjectiles[i][2], rifterProjectiles[i][3] # current and next X,Y
		p_X += p_XN * 10
		p_Y += p_YN * 10
		rifterProjectiles[i] = (p_X, p_Y, p_XN, p_YN)

	for projectile in rifterProjectiles:
		if projectile[0] < 0 or projectile[1] < 0 or projectile[0] > screenWidth or projectile[1] > screenHeight:
			rifterProjectiles.remove(projectile)

	surface.fill(0)
	rifter = pygame.transform.rotate(rifterSprite, rifterDirection - 180)
	rifterBlitPosition = [rifterPosition[0] - rifter.get_rect().width / 2, rifterPosition[1] - rifter.get_rect().height / 2]
	surface.blit(rifter, rifterBlitPosition)

	for projectile in rifterProjectiles:
		pygame.draw.rect(surface, (255,255,255), [int(projectile[0]) - 1, int(projectile[1]) - 1, 3, 3])


	pygame.transform.scale2x(surface, screen)
	pygame.display.update()
	
pygame.quit()
exit(0)