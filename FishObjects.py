import pygame

screen_width = 1280
screen_height = 720

class baseObject():
    def __init__(self, pos, vel, imageName):
        self.pos = pos
        self.vel = vel
        self.image = pygame.image.load(imageName)


    def update(self, deltaTime):
        self.pos[0] += self.vel[0] * deltaTime
        self.pos[1] += self.vel[1] * deltaTime
        # if self.pos.x < 0 or self.pos.x > screen_width - self.mWidth:
        #     self.mVelocity.x *= -1
        # if self.y < 0 or self.y > screen_height - self.mHeight:
        #     self.mVelocity.y *= -1

    def draw(self, window):
        window.blit(self.image, (self.pos.i))


    def add_force(self, forceVec):
        pass


class Fish(baseObject):
    def __init__(self, pos, vel, imageName):
        super().__init__(pos, vel, imageName)
        pass


class Treasure(baseObject):
    def __init__(self, pos, vel, imageName):
        super().__init__(pos, vel, imageName)
        pass