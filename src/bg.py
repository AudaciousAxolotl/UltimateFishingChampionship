import pygame


class Background(object):
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.pos = (self.posX, self.posY)

    def draw(self, img, screen):
        screen.blit(img, img.pos)

    def move(self, speed, direction):
        pass
