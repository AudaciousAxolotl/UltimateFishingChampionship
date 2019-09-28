import pygame
from vector import *


class Boatman:
    def __init__(self, pos=Vector2(0,0)):
        self.mPos = pos
        self.mVelocity = Vector2(0,0)
        self.mAcceleration = Vector2(0,0)
        self.mImage = None
        self.mMaxSpeed = 75
        self.mMaxSpeedSq = self.mMaxSpeed * self.mMaxSpeed


    def update(self, delta_time):
        self.mVelocity += self.mAcceleration * delta_time
        self.mAcceleration = Vector2(0,0)
        self.mPos += self.mVelocity * delta_time

    def add_force(self, force_vec2):
        self.mAcceleration += force_vec2

    def draw(self, screen):
        screen.blit(self.mImage, (int(self.x), int(self.y)))

    @property
    def x(self):
        return self.mPos.x

    @x.setter
    def x(self, new_x):
        self.mPos.x = new_x

    @property
    def y(self):
        return self.mPos.y

    @y.setter
    def y(self, new_y):
        self.mPos.y = new_y