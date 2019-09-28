import pygame


class baseObject():
    def __init__(self, pos, vel, imageName):
        self.pos = pos
        self.vel = vel
        self.image = pygame.image.load(imageName)


    def update(self, deltaTime):
        self.pos[0] += self.vel[0] * deltaTime
        self.pos[1] += self.vel[1] * deltaTime

    def draw(self, window):
        window.blit(self.image, (self.pos.i))

    def add_force(self, forceVec):
        pass


class Fish(baseObject):
    def __init__(self, pos, vel):
        super.__init__(pos, vel)
        pass


class Treasure(baseObject):
    def __init__(self, pos, vel):
        super.__init__(pos, vel)
        pass