import pygame

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
        self.height = self.images[1].get_height()
        self.currentImage = 0
        self.isCaught = False
        self.animTimer = 0.2
        self.animationCount = 0



    def update(self, deltaTime):
        # if self.isCaught:
        #     self.vel = self.boatPos - self.pos
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

    def draw(self, window):
        window.blit(self.images[self.currentImage], (self.pos.i))
        #self.currentImage = (self.currentImage + 1) % self.numOfImages


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