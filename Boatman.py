import pygame
from vector import *
import object


screen_width = 1280
screen_height = 720

class Boatman:
    mCastLaunchPoint: Vector2
    mCurrentLineTarget: Vector2
    mCurrentBobberLocation: Vector2

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
        self.mCastTime = 3.0
        self.mHalfCastTime = self.mCastTime / 2
        self.mMaxSpeedSq = self.mMaxSpeed * self.mMaxSpeed
        self.mWidth = self.mImage.get_width()
        self.mHalfWidth = self.mWidth / 2
        self.mHeight = self.mImage.get_height()
        self.mHalfHeight = self.mHeight / 2
        self.mBobberSize = 5
        self.mCurrentLineTarget = None
        self.mCurrentBobberLocation = None
        self.mCastLaunchPoint = None
        self.mCastingOut = False
        self.mReelingIn = False
        self.mCastingVector = None
        self.mAllowMovement = False
        self.mCaughtSomething = False
        self.mTargetReticleLocation = Vector2(screen_width/2, screen_height/2)
        self.mTargetReticleSpeed = 15
        self.mTargetReticleSize = 25
        self.mBobberCollisionSphere = object.Sphere((255,0,0), Vector2(-1000, -1000), self.mBobberSize)

    def update(self, delta_time):
        if self.mAllowMovement:
            if self.mNextCastTimer > 0:
                self.mNextCastTimer -= delta_time
                if self.mNextCastTimer < 0:
                    self.mNextCastTimer = 0
                    self.mCurrentLineTarget = None
                    self.mReelingIn = False
                    self.mCastingOut = False
                    self.mCastLaunchPoint = None
                    self.mCaughtSomething = False
                    self.mBobberCollisionSphere.mPos = Vector2(-1000,-1000)
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
            if self.mReelingIn:
                # replace this w/ a different, less linear function for fast followed by slow reel in
                percentReeled = (self.mHalfCastTime - self.mNextCastTimer) / self.mHalfCastTime
                self.mCurrentBobberLocation = self.mCurrentLineTarget - (percentReeled * (self.mCurrentLineTarget - self.fishing_pole_tip))
            if self.mCastingOut:
                percentCast = (self.mCastTime - self.mNextCastTimer) / self.mNextCastTimer
                if self.mNextCastTimer < self.mHalfCastTime:
                    self.mCastingOut = False
                    self.mReelingIn = True
                    percentCast = 1.0
                self.mCurrentBobberLocation = self.mCastLaunchPoint + (percentCast * self.mCastingVector)
        else:
            self.mVelocity = Vector2(0, 0)
            self.mNextCastTimer = 0
            self.mCastingOut = False
            self.mReelingIn = False
            self.mAcceleration = Vector2(0, 0)
            self.mCurrentLineTarget = None
            self.mCastLaunchPoint = None
        if self.mCastingOut or self.mReelingIn:
            self.mBobberCollisionSphere.mPos = self.mCurrentBobberLocation

    def checkBobberCollision(self, cuboid):
        if not self.mCaughtSomething and object.collides(self.mBobberCollisionSphere, cuboid):
            self.mCurrentLineTarget = self.mCurrentBobberLocation
            self.mCaughtSomething = True
            if self.mCastingOut:
                self.mNextCastTimer = self.mHalfCastTime
                self.mCastingOut = False
                self.mReelingIn = True
            return True
        return False


    def add_force(self, force_vec2):
        if self.mAllowMovement:
            self.mAcceleration += force_vec2

    def draw(self, screen):
        screen.blit(self.mImage, (int(self.x), int(self.y)))
        if self.mCurrentLineTarget is not None:
            pygame.draw.line(screen, (255, 255, 255), self.fishing_pole_tip.i, self.mCurrentBobberLocation.i, 3)
            pygame.draw.circle(screen, (255, 40, 80), self.mCurrentBobberLocation.i, 5)
        pygame.draw.circle(screen, (0, 0, 255), self.mTargetReticleLocation.i, self.mTargetReticleSize, 2)
        pygame.draw.line(screen, (0, 0, 255), (self.mTargetReticleLocation + Vector2(0, self.mTargetReticleSize)).i, (self.mTargetReticleLocation - Vector2(0, self.mTargetReticleSize)).i, 2)
        pygame.draw.line(screen, (0, 0, 255), (self.mTargetReticleLocation + Vector2(self.mTargetReticleSize, 0)).i, (self.mTargetReticleLocation - Vector2(self.mTargetReticleSize, 0)).i, 2)
        # self.mBobberCollisionSphere.drawPygame(screen, False, False)

    def cast_at(self, target_vector, directly_at_location=False):
        if self.mAllowMovement:
            if self.mCurrentLineTarget is None:
                self.mNextCastTimer = self.mCastTime
                if directly_at_location:
                    self.mCurrentLineTarget = target_vector
                else:
                    self.mCurrentLineTarget = self.fishing_pole_tip + (target_vector * self.mLineCastStrength)
                self.mCurrentBobberLocation = self.fishing_pole_tip
                self.mCastingVector = self.mCurrentLineTarget - self.mCurrentBobberLocation
                self.mCastLaunchPoint = self.mCurrentBobberLocation
                self.mCastingOut = True
                self.mReelingIn = False

    def cast_to(self, target_pos_vector):
        self.cast_at(target_pos_vector, True)

    def cast_line(self):
        self.cast_to(self.mTargetReticleLocation)

    def turn_on_movement(self):
        self.mAllowMovement = True

    def turn_off_movement(self):
        self.mAllowMovement = False

    def set_target_reticle(self, screen_pos_vector):
        self.mTargetReticleLocation = screen_pos_vector

    def move_target_reticle(self, change_vector):
        self.mTargetReticleLocation += change_vector * self.mTargetReticleSpeed
        if self.mTargetReticleLocation.x < 0:
            self.mTargetReticleLocation.x = 0
        if self.mTargetReticleLocation.y < 0:
            self.mTargetReticleLocation.y = 0
        if self.mTargetReticleLocation.x > screen_width:
            self.mTargetReticleLocation.x = screen_width
        if self.mTargetReticleLocation.y > screen_height:
            self.mTargetReticleLocation.y = screen_height

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

    @property
    def fishing_pole_tip(self):
        return Vector2(self.x + self.mHalfWidth, self.y + self.mHalfHeight)

    def bobber_location(self):
        return self.mCurrentBobberLocation
