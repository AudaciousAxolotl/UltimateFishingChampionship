import pygame, time, random, Boatman, FishObjects, itertools
from copy import deepcopy
from vector import *
from object import *
from bg import *
from star import *

pygame.display.init()
pygame.mixer.init()
pygame.font.init()
pygame.joystick.init()
clock = pygame.time.Clock()
win_width = 1280
win_height = 720
screen = pygame.display.set_mode((win_width, win_height))
background = pygame.image.load("Main_Scene.jpg")
waterScene = pygame.image.load("FISH_water.jpg")
bg = Background(background, 0, 0)
done = False
debugIsOn = False
joystick = None
joystickTriggerDown = False
joystickTriggerDownEvent = False
joystickTriggerUpEvent = False
pauseUpdates = False
updatePauseTime = 0.4
updatePauseTimer = 0
leftRightAxis = 0
upDownAxis = 0
castVectorAxis = Vector2(0, 0)
triggerAxis = 0
deadZoneThreshold=0.085
screenMoveUp = 0
starfieldMoveUp = 0

### Screen Shake Stuff ###
offset = itertools.repeat((0,0))
shakeScreen = screen.copy()

tintColor = (25,25,25)
tintAlpha = 200

fullScreenTintOverlay = screen.copy()
fullScreenTintOverlay.fill(tintColor)
fullScreenTintOverlay.set_alpha(tintAlpha)


def shake(multiplier):
    s = -1
    for _ in range(0, int(3*multiplier)):
        for x in range(0, int(20*multiplier), int(5*multiplier)):
            yield (random.choice(((x*s, 0), (0, x*s))))
        for x in range(int(20*multiplier), 0, int(5*multiplier)):
            yield (random.choice(((x*s, 0), (0, x*s))))
        s *= -1
    while True:
        yield (0, 0)

### End of non-gameloop screen shake stuff ###

starsArray = []
for i in range(50):
    starsArray.append(star(Vector2(random.randint(0,1280), random.randint(0, 720)),
                           3,1))

for i in range(50):
    starsArray.append(star(Vector2(random.randint(0,1280), random.randint(0, 720)),
                           5,3))

for i in range(50):
    starsArray.append(star(Vector2(random.randint(0,1280), random.randint(0, 720)),
                           7,5))

fishPics =[["Boot_1.png", "Boot_2.png"],
           ["Coin_1.png", "Coin_2.png"],
           ["Crab_1.png", "Crab_2.png"],
           ["fish_1.png", "fish_2.png"],
           ["Peach_1.png", "Peach_2.png"],
           ["Shell_1.png", "Shell_2.png"],
           ["Skull_1.png", "Skull_2.png"]]

fishLeftPics =[["Boot_1_l.png", "Boot_2_l.png"],
           ["Coin_1_l.png", "Coin_2_l.png"],
           ["Crab_1_l.png", "Crab_2_l.png"],
           ["fish_1_l.png", "fish_2_l.png"],
           ["Peach_1_l.png", "Peach_2_l.png"],
           ["Shell_1_l.png", "Shell_2_l.png"],
           ["Skull_1_l.png", "Skull_2_l.png"]]

myBoatman = Boatman.Boatman()
myFishList = []
caughtFishList = []
for i in range(10):
    myFish = FishObjects.Fish(Vector2(random.randint(100, 1180), random.randint(100, 620)),
                              Vector2(random.choice((-1, 1)) * random.randint(40, 80), random.choice((-1, 1)) * random.randint(30, 65)),
                              fishPics[i % 7], fishLeftPics[i % 7], Vector2(random.randint(1200,2400), random.randint(-250, -150)))
    myFishList.append(myFish)


BOB = FishObjects.Bob(Vector2(333, 550), Vector2(100, 0), ["Bob_1.png", "Bob_2.png", "Bob_3.png", "Bob_4.png"], ["Bob_1.png", "Bob_2.png", "Bob_3.png", "Bob_4.png"])

joystick_count = pygame.joystick.get_count()

if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

runningTime = 0

stardewFont = pygame.font.Font("font/Stardew_Valley.otf", 100)
title1X = 650
title2X = 700


introSequence = True
putBobInBoat = True

# This will be the first game loop, it will handle the intro sequence. Once the game starts, this loop will end and the
# next loop will begin.
while introSequence:
    ### UPDATES
    deltaTime = clock.tick() / 1000.0
    runningTime += deltaTime
    myBoatman.update(deltaTime)
    if not BOB.isDead:
        BOB.update(deltaTime)

    if runningTime >= 4.0: #was 5.0
        BOB.die()
        if putBobInBoat:
            putBobInBoat = False
            myBoatman.put_bob_in_boat()
        bg.move_right(3.98) #was 2.78
        if bg.posX < -1280:
            bg.posX = -1280

    ### INPUT
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            done = True
            introSequence = False
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                done = True
                introSequence = False
            if evt.key == pygame.K_F6:
                debugIsOn = not debugIsOn
    ### DRAWING

    #screen.fill((0, 0, 0))
    shakeScreen.fill((0, 0, 0))
    bg.draw(background, shakeScreen)
    myBoatman.draw(shakeScreen)
    if not BOB.isDead:
        BOB.draw(shakeScreen)

    title1 = pygame.font.Font.render(stardewFont, "Ultimate Fishing", True, (255, 255, 255))
    title2 = pygame.font.Font.render(stardewFont, "Championship", True, (255, 255, 255))
    control_string = "RT to"
    if joystick is None:
        control_string = "Left click to"
    instructions1 = pygame.font.Font.render(stardewFont, control_string, True, (255, 255, 255))
    instructions2 = pygame.font.Font.render(stardewFont, "catch fish", True, (255, 255, 255))

    if runningTime < 10.0:
        shakeScreen.blit(title1, (title1X, 150))
        shakeScreen.blit(title2, (title2X, 250))

    if runningTime >= 10.0:
        shakeScreen.blit(instructions1, ((1280 / 2 - (instructions1.get_width() / 2)), 150))
        shakeScreen.blit(instructions2, ((1280 / 2 - (instructions1.get_width()) + 12), 250))
        introSequence = False


    if 10.0 < runningTime < 11.0:
        if myBoatman.mVelocity.x <= 0:
            myBoatman.mVelocity = Vector2(0, 0)

    if runningTime >= 5.0:
        myBoatman.mAllowMovement = True
        myBoatman.add_force(Vector2(-11, 0))
        title1X -= 3
        if title1X <= (1280 / 2 - (title1.get_width() / 2)):
            title1X = (1280 / 2 - (title1.get_width() / 2))
        title2X -= 3
        if title2X <= (1280 / 2 - (title2.get_width() / 2)):
            title2X = (1280 / 2 - (title2.get_width() / 2) - 1)

    if runningTime >= 10.0:
        bg.move_down(6.87)
        if bg.posY < -720:
            bg.posY = 720

    screen.blit(shakeScreen, next(offset))
    pygame.display.flip()


myBoatman.turn_on_movement()
gameStarted = False

#Game Loop in dis bish
while not done:
    #################################
    #                               #
    #       UPDATES                 #
    #                               #
    #################################
    deltaTime = clock.tick(60) / 1000.0
    if gameStarted:
        screenMoveUp -= 7

    if pauseUpdates:
        updatePauseTimer -= deltaTime
        if updatePauseTimer < 0:
            pauseUpdates = False
            updatePauseTimer = 0

    if not pauseUpdates:
        for fish in myFishList:
            fish.update(deltaTime)

        for i in range (0, len(myFishList)):
            for j in range(i+1, len(myFishList)):
                if i != j and checkRectCollision(myFishList[i].colliderCuboid, myFishList[j].colliderCuboid):
                    if myFishList[i].readyToFlutter and myFishList[j].readyToFlutter \
                            and not myFishList[i].collidedWith and not myFishList[j].collidedWith:
                        #TODO play fish collision sound
                        collisionVector = (myFishList[i].center_pos - myFishList[j].center_pos).normalized
                        myFishList[i].vel = myFishList[i].vel.magnitude * collisionVector
                        myFishList[j].vel = myFishList[j].vel.magnitude * -collisionVector
                        myFishList[i].center_pos += (0.5 * collisionVector)
                        myFishList[j].center_pos -= (0.5 * collisionVector)

        for star in starsArray:
            star.move()

        myBoatman.add_force(Vector2(leftRightAxis * myBoatman.mMoveSpeed, upDownAxis * myBoatman.mMoveSpeed))
        myBoatman.update(deltaTime)

        if not myBoatman.mCaughtSomething:
            for fish in myFishList:
                if fish.isCaught:
                    fish.die()
                    offset = shake(1.0)
                    #TODO: play item/fish caught sound
                else:
                    fish.isCaught = myBoatman.checkBobberCollision(fish.colliderCuboid)
                    if fish.isCaught:
                        offset = shake(0.5)
                        pauseUpdates = True
                        updatePauseTimer = updatePauseTime
                        break
        else:
            for fish in myFishList:
                if fish.isCaught:
                    fish.center_pos = myBoatman.bobber_location

        myFishList[:] = [fish for fish in myFishList if not fish.isDead]




    #################################
    #                               #
    #       INPUT                   #
    #                               #
    #################################

    if joystick is None:
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        if not pauseUpdates:
            myBoatman.set_target_reticle(Vector2(mouse_x, mouse_y))

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            done = True
        if not pauseUpdates:
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_ESCAPE:
                    done = True
                if evt.key == pygame.K_F6:
                    debugIsOn = not debugIsOn

            if evt.type == pygame.MOUSEBUTTONDOWN:
                if evt.button == 1:
                    if joystick is None:
                        myBoatman.cast_line()
                        gameStarted = True
                        for fish in myFishList:
                            fish.fly_in()

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

    if joystick is not None:
        leftRightAxis = joystick.get_axis(0)
        upDownAxis = joystick.get_axis(1)
        castVectorAxis = Vector2(joystick.get_axis(4), joystick.get_axis(3))
        triggerAxis = joystick.get_axis(2)

    key_pressed = pygame.key.get_pressed()

    if not pauseUpdates:
        if key_pressed[pygame.K_j]:
            offset = shake(1.0)

        if key_pressed[pygame.K_k]:
            offset = shake(2.3)

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

        if joystick is not None:
            myBoatman.move_target_reticle(castVectorAxis)


    #################################
    #                               #
    #       DRAWING                 #
    #                               #
    #################################

    screen.fill((0, 0, 0))
    shakeScreen.fill((51, 0, 102))
    for star in starsArray:
        star.draw(shakeScreen)
    shakeScreen.blit(waterScene, (0, screenMoveUp))
    #bg.draw(background, shakeScreen)

    myBoatman.draw(shakeScreen)
    for fish in myFishList:
        fish.draw(shakeScreen)

    if pauseUpdates:
        shakeScreen.blit(fullScreenTintOverlay, (0,0))
        myBoatman.draw(shakeScreen)
        caughtFishList[:] = [fish for fish in myFishList if fish.isCaught]
        caughtFishList[0].draw(shakeScreen)

    screen.blit(shakeScreen, next(offset))
    pygame.display.flip()


pygame.font.quit()
pygame.mixer.quit()
pygame.display.quit()