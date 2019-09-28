import pygame, time, random, Boatman
from vector import *

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
leftRightAxis = 0
upDownAxis = 0

myBoatman = Boatman.Boatman()

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

    print("(", leftRightAxis, ",", upDownAxis, ")")

    key_pressed = pygame.key.get_pressed()

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

    myBoatman.add_force(Vector2(leftRightAxis * myBoatman.mMoveSpeed, upDownAxis * myBoatman.mMoveSpeed))
    myBoatman.update(deltaTime)
    screen.blit(background, (0, 0))
    myBoatman.draw(screen)
    pygame.display.flip()

pygame.font.quit()
pygame.mixer.quit()
pygame.display.quit()