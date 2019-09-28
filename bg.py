import pygame
# from main import *


class Background(object):
    def __init__(self, image, posX, posY):
        self.image = image
        self.posX = posX
        self.posY = posY

    def draw(self, img, screen):
        screen.blit(img, (self.posX, self.posY))

    def move_down(self, speed):
        self.posY += speed

    def move_right(self, speed):
        self.posX -= speed
