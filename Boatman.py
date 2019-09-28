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
        self.mLineCastStrength = 500
        self.mNextCastTimer = 0
        self.mCastTime = 2.0
        self.mMaxSpeedSq = self.mMaxSpeed * self.mMaxSpeed
        self.mWidth = self.mImage.get_width()
        self.mHalfWidth = self.mWidth / 2
        self.mHeight = self.mImage.get_height()
        self.mHalfHeight = self.mHeight / 2
        self.mCurrentLineTarget = None


    def update(self, delta_time):
        if self.mNextCastTimer > 0:
            self.mNextCastTimer -= delta_time
            if self.mNextCastTimer < 0:
                self.mNextCastTimer = 0
                self.mCurrentLineTarget = None
        self.mVelocity += self.mAcceleration * delta_time
        self.mVelocity *= self.mDragCoefficient
        if self.mVelocity.magnitudeSq > self.mMaxSpeedSq:
            self.mVelocity = self.mVelocity.normalized * self.mMaxSpeed
        self.mAcceleration = Vector2(0, 0)
        self.mPos += self.mVelocity * delta_time
        if self.x < 0 and self.mVelocity.x < 0:
            self.mVelocity.x *= -1
        if self.x > screen_width - self.mWidth and self.mVelocity.x > 0:
            self.mVelocity.x *= -1
        if self.y < 0 and self.mVelocity.y < 0:
            self.mVelocity.y *= -1
        if self.y > screen_height - self.mHeight and self.mVelocity.y > 0:
            self.mVelocity.y *= -1


    def add_force(self, force_vec2):
        self.mAcceleration += force_vec2

    def draw(self, screen):
        screen.blit(self.mImage, (int(self.x), int(self.y)))
        if self.mCurrentLineTarget is not None:
            pygame.draw.line(screen, (255,255,255), self.mPos+Vector2(self.mHalfWidth, self.mHalfHeight), self.mCurrentLineTarget, 3)

    def cast_at(self, direction_vector):
        if self.mCurrentLineTarget is None:
            self.mNextCastTimer = self.mCastTime
            self.mCurrentLineTarget = self.mPos+Vector2(self.mHalfWidth, self.mHalfHeight) + (direction_vector * self.mLineCastStrength)

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