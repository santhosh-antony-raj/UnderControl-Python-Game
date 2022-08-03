import pygame
from pygame import mixer

import math
import random

# intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
Background = pygame.image.load("Background.png")

#background music
mixer.music.load("back1.wav")
mixer.music.play(-1)

# TITLE AND ICON
pygame.display.set_caption("Under Control")
icon = pygame.image.load("image.png.png")
pygame.display.set_icon(icon)

# player image size
playerImg = pygame.image.load("spaceinvaders.png")
playerX = 370
playerY = 480
playerX_change = 0
# enemy image size
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(40, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


# bullet image size # ready - we cant see the bullet on this position #fire now you can able to see the bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

def show_score(x, y):
    score = font.render("score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score,(x, y))
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# collision
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:

    # RGB - red green blue
    screen.fill((0, 0, 0))
    # background
    screen.blit(Background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke means ( giving control to the keys) to the player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                #get the current x coordinate of the spaceship
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # boundries for undercontrol
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    # enemy for under control
    for i in range(no_of_enemies):
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = (random.randint(0, 800))
            enemyY[i] = (random.randint(40, 150))
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement if bullet_state is 'fire'
    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change
    # more bullets
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"



    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
