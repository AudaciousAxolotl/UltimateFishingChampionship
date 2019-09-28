import pygame, time, random, Boatman
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

background = pygame.image.load("FISH_Starting_Level.jpg")

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

myBoatman = Boatman.Boatman()

bg = Background(background, 0, 0)

joystick_count = pygame.joystick.get_count()

if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

#Game Loop in dis bish
while not done:
    deltaTime = clock.tick() / 1000.0

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            done = True
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                done = True
            if evt.key == pygame.K_F6:
                debugIsOn = not debugIsOn

        if evt.type == pygame.JOYBUTTONDOWN:
            if evt.button == 0:
                print("A?")
            elif evt.button == 2:
                """ X Button """
                print("X!")
            elif evt.button == 3:
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
        castVectorAxis = Vector2(joystick.get_axis(4), joystick.get_axis(3)).normalized
        triggerAxis = joystick.get_axis(2)

    key_pressed = pygame.key.get_pressed()

    if joystickTriggerDown:
        if abs(triggerAxis) < 0.5:
            joystickTriggerDown = False
            joystickTriggerUpEvent = True
            print("Trigger up!")
    else:
        if abs(triggerAxis) > 0.7:
            joystickTriggerDown = True
            joystickTriggerDownEvent = True
            print("Trigger down!")

    if key_pressed[pygame.K_w]:
        upDownAxis = -0.6

    if key_pressed[pygame.K_s]:
        upDownAxis = 0.6

    if key_pressed[pygame.K_a]:
        leftRightAxis = -0.6

    if key_pressed[pygame.K_d]:
        leftRightAxis = 0.6

    if abs(leftRightAxis) < 0.07:
        leftRightAxis = 0

    if abs(upDownAxis) < 0.07:
        upDownAxis = 0

    if joystickTriggerDownEvent:
        myBoatman.cast_at(castVectorAxis)
        joystickTriggerDownEvent = False

    if joystickTriggerUpEvent:
        joystickTriggerUpEvent = False

    myBoatman.add_force(Vector2(leftRightAxis * myBoatman.mMoveSpeed, upDownAxis * myBoatman.mMoveSpeed))
    myBoatman.update(deltaTime)

    #screen.fill((0, 0, 0))

    #bg.move(20, deltaTime)

    bg.draw(background, screen)
    myBoatman.draw(screen)

    pygame.display.flip()

pygame.font.quit()
pygame.mixer.quit()
pygame.display.quit()