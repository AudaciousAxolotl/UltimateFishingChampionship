import pygame, time

pygame.display.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()
win_width = 1280
win_height = 720
screen = pygame.display.set_mode((win_width, win_height))
background = pygame.image.load("FISH_Starting_Level.jpg")
done = False


#Game Loop in dis bish
while not done:
    deltaTime = clock.tick() / 1000.0
    pygame.display.flip()

pygame.font.quit()
pygame.mixer.quit()
pygame.display.quit()