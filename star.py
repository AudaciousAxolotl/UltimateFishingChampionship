from vector import *
import random, pygame


class star():
    def __init__(self, pos, speed, radius):
        self.pos = pos
        self.speed = speed
        self.radius = radius

    def move(self):
        self.pos[1] -= self.speed
        if self.pos.y <= 0:
            self.pos.y = 720
            self.pos[0] = random.randint(0,1280)

    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), self.pos.i, self.radius)