import pygame
from vector import *
import object


screen_width = 1280
screen_height = 720

class Boatman:
    mCastLaunchPoint: Vector2
    mCurrentLineTarget: Vector2
    mCurrentBobberLocation: Vector2

    def __init__(self, pos=Vector2(772, 600)):
        self.mPos = pos
        self.mVelocity = Vector2(0, 0)
        self.mAcceleration = Vector2(0, 0)
        self.mDrag = Vector2(0,0)
        self.mDragCoefficient = 0.995
        self.mBobInBoat = False
        self.mBobCastingFrames = {}
        # 1 = right, -1 = left
        self.mCurrentCastDirection = 1
        self.mCurrentCastFrame = 1
        self.mAnimationTimer = 0
        for i in range(1, 7):
            self.mBobCastingFrames[(1, i)] = pygame.image.load("Bob_F_" + str(i) + ".png")
            self.mBobCastingFrames[(-1, i)] = pygame.image.load("Bob_F_L_" + str(i) + ".png")
        self.mBoatImage = pygame.image.load("BoatScaled.png")
        self.mImage = self.mBoatImage
        self.mMoveSpeed = 200
        self.mMaxSpeed = 300
        self.mLineCastStrength = 500
        self.mNextCastTimer = 0
        self.mCastTime = 2.0
        self.mHalfCastTime = self.mCastTime / 2
        self.mMaxSpeedSq = self.mMaxSpeed * self.mMaxSpeed
        self.mWidth = self.mBobCastingFrames[(self.mCurrentCastDirection, self.mCurrentCastFrame)].get_width()
        self.mHalfWidth = self.mWidth / 2
        self.mHeight = self.mBobCastingFrames[(self.mCurrentCastDirection, self.mCurrentCastFrame)].get_height()
        self.mHalfHeight = self.mHeight / 2
        self.mFrameHeightDiff = self.mHeight - self.mImage.get_height()
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
        self.mBobberCollisionBox = object.QuickAndDirtyCollisionRect(self.mPos - Vector2(self.mBobberSize, self.mBobberSize), self.mBobberSize * 2, self.mBobberSize * 2)

        self.mPoleLocation = {(1, 1): Vector2(178, 63),
                              (1, 2): Vector2(168, 15),
                              (1, 3): Vector2(161, 9),
                              (1, 4): Vector2(161, 9),
                              (1, 5): Vector2(168, 15),
                              (1, 6): Vector2(177, 62),
                              (-1, 1): Vector2(46, 19),
                              (-1, 2): Vector2(81, 23),
                              (-1, 3): Vector2(53, 10),
                              (-1, 4): Vector2(53, 10),
                              (-1, 5): Vector2(53, 10),
                              (-1, 6): Vector2(36, 63)}
        self.mCurrentAnimationNumber = -1
        self.mCurrentAnimationStep = 0
        self.mAnimating = False
        # 0 = casting
        # 1 = reeling
        # 2 = back to static
        self.mAnimations = [[(1, 0.05), (2, 0.1), (3, -1)],
                            [(3, 0.08), (5, -1)],
                            [(5, 0.05), (1, -1)]]

    def update(self, delta_time):
        if self.mAllowMovement:
            if self.mAnimating:
                self.mAnimationTimer -= delta_time
                if self.mAnimationTimer < 0:
                    self.mCurrentAnimationStep += 1
                    self.mAnimationTimer = self.mAnimations[self.mCurrentAnimationNumber][self.mCurrentAnimationStep][1]
                    self.mCurrentCastFrame = self.mAnimations[self.mCurrentAnimationNumber][self.mCurrentAnimationStep][0]
                    if self.mAnimationTimer == -1:
                        self.mAnimating = False
            if self.mCastingOut or self.mReelingIn:
                self.mNextCastTimer -= delta_time
                if self.mNextCastTimer < 0:
                    self.mNextCastTimer = 0
                    self.mCurrentLineTarget = None
                    self.mReelingIn = False
                    self.mCastingOut = False
                    self.mCastLaunchPoint = None
                    self.mCaughtSomething = False
                    self.mBobberCollisionBox.set_pos(Vector2(-1000,-1000))
                    self.play_animation(2)
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
                    self.play_animation(1)
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
            self.mBobberCollisionBox.set_pos(self.mCurrentBobberLocation - Vector2(self.mBobberSize, self.mBobberSize))

    def checkBobberCollision(self, box):
        if not self.mCaughtSomething and self.mBobberCollisionBox.collides(box):
            self.mCurrentLineTarget = box.center
            self.mCurrentBobberLocation = self.mCurrentLineTarget
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
        if self.mBobInBoat:
            self.mImage = self.mBobCastingFrames[(self.mCurrentCastDirection, self.mCurrentCastFrame)]
        screen.blit(self.mImage, (int(self.x), int(self.y)))
        if self.mCurrentLineTarget is not None:
            pygame.draw.line(screen, (255, 255, 255), self.fishing_pole_tip.i2, self.mCurrentBobberLocation.i2, 3)
            pygame.draw.circle(screen, (255, 40, 80), self.mCurrentBobberLocation.i2, 5)
        pygame.draw.circle(screen, (0, 0, 255), self.mTargetReticleLocation.i2, self.mTargetReticleSize, 2)
        pygame.draw.line(screen, (0, 0, 255), (self.mTargetReticleLocation + Vector2(0, self.mTargetReticleSize)).i2, (self.mTargetReticleLocation - Vector2(0, self.mTargetReticleSize)).i2, 2)
        pygame.draw.line(screen, (0, 0, 255), (self.mTargetReticleLocation + Vector2(self.mTargetReticleSize, 0)).i2, (self.mTargetReticleLocation - Vector2(self.mTargetReticleSize, 0)).i2, 2)

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
                if self.mCastingVector.x < 0:
                    self.mCurrentCastDirection = -1
                else:
                    self.mCurrentCastDirection = 1
                self.mCastLaunchPoint = self.mCurrentBobberLocation
                self.mCastingOut = True
                self.mReelingIn = False
                self.play_animation(0)

    def cast_to(self, target_pos_vector):
        self.cast_at(target_pos_vector, True)

    def cast_line(self):
        if not self.mCastingOut and not self.mReelingIn:
            self.cast_to(self.mTargetReticleLocation)
        elif self.mCastingOut:
            if self.mNextCastTimer - self.mHalfCastTime > 0:
                self.play_animation(1)
                self.mNextCastTimer = self.mCastTime - self.mNextCastTimer
                self.mCastingOut = False
                self.mReelingIn = True

    def put_bob_in_boat(self):
        if not self.mBobInBoat:
            self.mBobInBoat = True
            self.mPos -= Vector2(0, self.mFrameHeightDiff)

    def take_bob_out_of_boat(self):
        self.mBobInBoat = False
        self.mPos += Vector2(0, self.mFrameHeightDiff)
        self.mImage = self.mBoatImage

    def turn_on_movement(self):
        self.mAllowMovement = True
        self.put_bob_in_boat()

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

    def play_animation(self, anim_number):
        self.mAnimating = True
        self.mCurrentAnimationNumber = anim_number
        self.mCurrentAnimationStep = 0
        self.mAnimationTimer = self.mAnimations[anim_number][0][1]

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
        return self.mPos + self.mPoleLocation[(self.mCurrentCastDirection, self.mCurrentCastFrame)]

    @property
    def bobber_location(self):
        return self.mCurrentBobberLocation

