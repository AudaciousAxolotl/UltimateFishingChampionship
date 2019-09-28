import pygame
import time
from bg import *

pygame.init()

screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()

testimg1 = pygame.image.load("FISH_water.jpg")
#testimg2 = pygame.image.load("testimg2.jpg")

bg = Background(testimg1, 0, 0)
#bg2 = Background(testimg2, 500, 0)

while True:
    deltaTime = clock.tick()/1000.0

    pygame.event.pump() #ToDo figure out what this does

    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        pygame.display.quit()
    if key[]

    screen.fill((0, 0, 0))

    bg.move(20, deltaTime)
    #bg2.move(40, deltaTime)

    bg.draw(bg.image, screen)
    #bg2.draw(bg2.image, screen)

    print(bg.posY)

    pygame.display.update()

