import pygame
import object
from vector import *
from vector import *

screen_width = 1280
screen_height = 720

class baseObject():
    def __init__(self, pos, vel, *images):
        self.pos = pos
        self.vel = vel
        self.images = []
        for image in images:
            self.images.append(pygame.image.load(image))
        self.numOfImages = len(self.images)
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.halfWidth = self.width / 2
        self.halfHeight = self.height / 2
        self.currentImage = 0
        self.isCaught = False
        self.isDead = False
        self.animTimer = 0.2
        self.animationCount = 0
        self.colliderCuboid = object.Cuboid((255,0,255), self.pos + Vector2(self.halfWidth, self.halfHeight), (self.width, self.height))
        self.colliderCuboid.rotate(90)

    def update(self, deltaTime):
        if not self.isCaught:
            self.pos[0] += self.vel[0] * deltaTime
            self.pos[1] += self.vel[1] * deltaTime
            self.animationCount += deltaTime
            if self.animationCount >= self.animTimer:
                self.currentImage = (self.currentImage + 1) % self.numOfImages
                self.animationCount = 0

            if self.pos.x < 0 or self.pos.x > screen_width - self.width:
                self.vel.x *= -1
            if self.pos.y < 0 or self.pos.y > screen_height - self.height:
                self.vel.y *= -1

            self.colliderCuboid.updatePos(self.pos + Vector2(self.halfWidth, self.halfHeight))

    def draw(self, window):
        window.blit(self.images[self.currentImage], (self.pos.i2))
        #self.colliderCuboid.drawPygame(window, False, False)
        #self.currentImage = (self.currentImage + 1) % self.numOfImages

    def die(self):
        self.isDead = True

    def add_force(self, forceVec):
        pass


class Fish(baseObject):
    def __init__(self, pos, vel, *images):
        super().__init__(pos, vel, *images)
        pass

    def catch(self, boatPos):
        self.vel = boatPos - self.pos
        self.vel = self.vel.normalized * 600
        self.isCaught = True


class Treasure(baseObject):
    def __init__(self, pos, vel, imageName):
        super().__init__(pos, vel, imageName)
        pass