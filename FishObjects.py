import pygame
import object
from vector import *
from vector import *

screen_width = 1280
screen_height = 720

class baseObject():
    def __init__(self, pos, vel, images, left_images, offset_vec):
        self.basename = images[0][:-6]
        self.pos = pos
        self.startPos = pos
        self.vel = vel
        self.offset = Vector2(0, offset_vec.x)
        self.pos += self.offset
        self.offsetVel = Vector2(0, offset_vec.y)
        self.readyToFlyIn = False
        self.readyToFlutter = False
        self.collidedWith = False
        self.facingLeft = False
        self.images = []
        self.leftImages = []
        for image in images:
            self.images.append(pygame.transform.rotozoom(pygame.image.load(image), 0, 2))
        for left_image in left_images:
            self.leftImages.append(pygame.transform.rotozoom(pygame.image.load(left_image), 0, 2))
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
        self.colliderCuboid = object.QuickAndDirtyCollisionRect(self.pos, self.width, self.height)

    def update(self, deltaTime):
        if self.collidedWith:
            self.collidedWith = False
        if self.readyToFlutter:
            if not self.isCaught:
                self.pos += self.vel * deltaTime
                self.animationCount += deltaTime
                if self.animationCount >= self.animTimer:
                    self.currentImage = (self.currentImage + 1) % self.numOfImages
                    self.animationCount = 0

                if self.pos.x < 0 or self.pos.x > screen_width - self.width:
                    self.vel.x *= -1
                    self.facingLeft = not self.facingLeft
                    print(screen_width, self.width)

                if self.pos.y < 0 or self.pos.y > screen_height - self.height:
                    self.vel.y *= -1

                self.colliderCuboid.set_pos(self.pos)
        elif self.readyToFlyIn:
            self.pos += self.offsetVel * deltaTime
            if self.pos.y < self.startPos.y:
                self.pos = self.startPos
                self.readyToFlutter = True


    def draw(self, window):
        if self.facingLeft:
            window.blit(self.leftImages[self.currentImage], (self.pos.i2))
        else:
            window.blit(self.images[self.currentImage], (self.pos.i2))
        #self.colliderCuboid.drawPygame(window, False, False)
        #self.currentImage = (self.currentImage + 1) % self.numOfImages

    def die(self):
        self.isDead = True

    def add_force(self, forceVec):
        pass

    def fly_in(self):
        self.readyToFlyIn = True

    # def __del__(self):
    #     print("die")

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @property
    def center_pos(self):
        return self.pos + Vector2(self.halfWidth, self.halfHeight)

    @center_pos.setter
    def center_pos(self, new_center):
        self.pos = new_center - Vector2(self.halfWidth, self.halfHeight)

    def get_type(self):
        if self.basename in ["Boot", "Coin", "Crab", "Shell", "Skull"]:
            return "Hard"
        return "Soft"

class Fish(baseObject):
    def __init__(self, pos, vel, images, left_images, offset_vector):
        super().__init__(pos, vel, images, left_images, offset_vector)
        pass

    def catch(self, boatPos):
        self.vel = boatPos - self.pos
        self.vel = self.vel.normalized * 600
        self.isCaught = True

class Bob(baseObject):
    def __init__(self, pos, vel, left_images, right_images, offset_vec = Vector2(0, 0)):
        super().__init__(pos, vel, left_images, right_images, offset_vec)
        self.readyToFlyIn = False
        self.readyToFlutter = True
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.rotozoom(self.images[i],0,  0.15)
            self.leftImages[i] = pygame.transform.rotozoom(self.leftImages[i], 0, 0.15)

        self.width = self.images[0].get_width()