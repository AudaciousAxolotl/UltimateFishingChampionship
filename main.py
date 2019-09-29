import pygame, time, random, Boatman, FishObjects, itertools
from vector import *
from bg import *

pygame.display.init()
pygame.mixer.init()
pygame.font.init()
pygame.joystick.init()
clock = pygame.time.Clock()
win_width = 1280
win_height = 720
screen = pygame.display.set_mode((win_width, win_height))
background = pygame.image.load("Main_Scene.jpg")
bg = Background(background, 0, 0)

done = False
debugIsOn = False
joystick = None
joystickTriggerDown = False
joystickTriggerDownEvent = False
joystickTriggerUpEvent = False
leftRightAxis = 0
upDownAxis = 0
castVectorAxis = Vector2(0, 0)
triggerAxis = 0
deadZoneThreshold=0.085

### Screen Shake Stuff ###
offset = itertools.repeat((0,0))
shakeScreen = screen.copy()

def shake():
    s = -1
    for _ in range(0, 3):
        for x in range(0, 20, 5):
            yield (x*s, 0)
        for x in range(20, 0, 5):
            yield (x*s, 0)
        s *= -1
    while True:
        yield (0, 0)

### End of non-gameloop screen shake stuff ###


myBoatman = Boatman.Boatman()
myBoatman.turn_on_movement()
myFishList = []
for i in range(5):
    myFish = FishObjects.Fish(Vector2(random.randint(100, 1180), random.randint(100, 620)),
                              Vector2(random.randint(-20, 20), random.randint(-20, 20)), "fish_temp.jpg")
    myFishList.append(myFish)

joystick_count = pygame.joystick.get_count()

if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

runningTime = 0

pygame.font.init()
stardewFont = pygame.font.Font("font/Stardew_Valley.otf", 100)
title1X = 650
title2X = 700

#Game Loop in dis bish
while not done:
    deltaTime = clock.tick() / 1000.0
    runningTime += deltaTime

    if joystick is None:
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        myBoatman.set_target_reticle(Vector2(mouse_x, mouse_y))

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            done = True
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                done = True
            if evt.key == pygame.K_F6:
                debugIsOn = not debugIsOn

        if evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1:
                if joystick is None:
                    myBoatman.cast_line()

        if evt.type == pygame.JOYBUTTONDOWN:
            if evt.button == 0:
                if debugIsOn:
                    print("A?")
            elif evt.button == 2:
                """ X Button """
                if debugIsOn:
                    print("X!")
            elif evt.button == 3:
                if debugIsOn:
                    print("Y!")
            elif evt.button == 6:
                done = True
            elif evt.button == 7:
                debugIsOn = not debugIsOn
            else:
                if debugIsOn:
                    print("Joystick button pressed: ", str(evt.button))
#            if evt.button == 5:
#                """ Right Bumper """

#            if evt.button == 4:
#                """ Left Bumper """

    if joystick is not None:
        leftRightAxis = joystick.get_axis(0)
        upDownAxis = joystick.get_axis(1)
        castVectorAxis = Vector2(joystick.get_axis(4), joystick.get_axis(3))
        triggerAxis = joystick.get_axis(2)

    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_j]:
        offset = shake()

    if joystickTriggerDown:
        if abs(triggerAxis) < 0.5:
            joystickTriggerDown = False
            joystickTriggerUpEvent = True
            if debugIsOn:
                print("Trigger up!")
    else:
        if abs(triggerAxis) > 0.7:
            joystickTriggerDown = True
            joystickTriggerDownEvent = True
            if debugIsOn:
                print("Trigger down!")

    if joystick is None:
        if key_pressed[pygame.K_w]:
            upDownAxis = -0.6
        else:
            if key_pressed[pygame.K_s]:
                upDownAxis = 0.6
            else:
                upDownAxis = 0

        if key_pressed[pygame.K_a]:
            leftRightAxis = -0.6
        else:
            if key_pressed[pygame.K_d]:
                leftRightAxis = 0.6
            else:
                leftRightAxis = 0

    if abs(leftRightAxis) < deadZoneThreshold:
        leftRightAxis = 0

    if abs(upDownAxis) < deadZoneThreshold:
        upDownAxis = 0

    if abs(castVectorAxis.x) < deadZoneThreshold:
        castVectorAxis.x = 0

    if abs(castVectorAxis.y) < deadZoneThreshold:
        castVectorAxis.y = 0

    if joystickTriggerDownEvent:
        myBoatman.cast_line()
        joystickTriggerDownEvent = False

    if joystickTriggerUpEvent:
        joystickTriggerUpEvent = False

    myBoatman.add_force(Vector2(leftRightAxis * myBoatman.mMoveSpeed, upDownAxis * myBoatman.mMoveSpeed))
    myBoatman.update(deltaTime)
    for fish in myFishList:
        fish.update(deltaTime)

    if joystick is not None:
        myBoatman.move_target_reticle(castVectorAxis)

    if not myBoatman.mCaughtSomething:
        for fish in myFishList:
            if fish.isCaught:
                fish.die()
            else:
                fish.isCaught = myBoatman.checkBobberCollision(fish.colliderCuboid)
                if fish.isCaught:
                    break
    else:
        for fish in myFishList:
            if fish.isCaught:
                fish.pos=myBoatman.mCurrentBobberLocation

    myFishList[:] = [fish for fish in myFishList if not fish.isDead]

    screen.fill((0, 0, 0))
    shakeScreen.fill((0, 0, 0))

    if runningTime >= 2.0:
        bg.move_right(2.78)
        if bg.posX < -1280:
            bg.posX = -1280

    bg.draw(background, shakeScreen)

    for fish in myFishList:
        fish.draw(shakeScreen)

    myBoatman.draw(shakeScreen)

    title1 = pygame.font.Font.render(stardewFont, "Ultimate Fishing", True, (255, 255, 255))
    title2 = pygame.font.Font.render(stardewFont, "Championship", True, (255, 255, 255))
    instructions1 = pygame.font.Font.render(stardewFont, "RT to", True, (255, 255, 255))
    instructions2 = pygame.font.Font.render(stardewFont, "catch fish", True, (255, 255, 255))

    if runningTime < 10.0:
        shakeScreen.blit(title1, (title1X, 150))
        shakeScreen.blit(title2, (title2X, 250))
    if runningTime >= 10.0:
        shakeScreen.blit(instructions1, ((1280/2 - (instructions1.get_width()/2)), 150))
        shakeScreen.blit(instructions2, ((1280/2 - (instructions1.get_width())+12), 250))
        myBoatman.mAllowMovement = True

    if 10.0 < runningTime < 11.0:
        if myBoatman.mVelocity.x <= 0:
            myBoatman.mVelocity = Vector2(0, 0)

    if runningTime >= 2.0:
        myBoatman.mAllowMovement = True
        myBoatman.add_force(Vector2(-11, 0))
        title1X -= 3
        if title1X <= (1280 / 2 - (title1.get_width() / 2)):
            title1X = (1280 / 2 - (title1.get_width() / 2))
        title2X -= 3
        if title2X <= (1280 / 2 - (title2.get_width() / 2)):
            title2X = (1280 / 2 - (title2.get_width() / 2) - 1)

    screen.blit(shakeScreen, next(offset))


    pygame.display.flip()

pygame.font.quit()
pygame.mixer.quit()
pygame.display.quit()