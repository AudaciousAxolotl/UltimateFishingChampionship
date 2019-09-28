import pygame
from vector import *

screen_width = 1280
screen_height = 720

class Boatman:
    def __init__(self, pos=Vector2(0, 0)):
        self.mPos = pos
        self.mVelocity = Vector2(0, 0)
        self.mAcceleration = Vector2(0, 0)
        self.mDrag = Vector2(0,0)
        self.mDragCoefficient = 0.995
        self.mImage = pygame.image.load("img/boatman.png")
        self.mMoveSpeed = 200
        self.mMaxSpeed = 300
        self.mMaxSpeedSq = self.mMaxSpeed * self.mMaxSpeed
        self.mWidth = self.mImage.get_width()
        self.mHeight = self.mImage.get_height()

    def update(self, delta_time):
        self.mVelocity += self.mAcceleration * delta_time
        self.mVelocity *= self.mDragCoefficient
        if self.mVelocity.magnitudeSq > self.mMaxSpeedSq:
            self.mVelocity = self.mVelocity.normalized * self.mMaxSpeed
        self.mAcceleration = Vector2(0, 0)
        self.mPos += self.mVelocity * delta_time
        if self.x < 0 or self.x > screen_width - self.mWidth:
            self.mVelocity.x *= -1
        if self.y < 0 or self.y > screen_height - self.mHeight:
            self.mVelocity.y *= -1


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