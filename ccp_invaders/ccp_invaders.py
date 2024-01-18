import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load('images/tiananmensqr.jpg')

# background sound
# -1 = loop
mixer.music.load('audio/background.wav')
mixer.music.play(-1)
# Title and  Icon
pygame.display.set_caption("CCP Invaders")
icon = pygame.image.load('images/player.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('images/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
# i = multiple enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/tank.png'))
    enemyX.append(random.randint(0, 720))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# bullet
# ready = invisible
# fire = visible
bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_value = 0
# font style, font size
font = pygame.font.Font('freesansbold.ttf',32)
# score coordinate
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

# score convert to string, rgb
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (playerX, playerY))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# d = √(x₂-x₁)² + (y₂-y₁)²
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False


# game loop
running = True
while running:
    clock.tick(fps)

    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke right left
        # x = x + -0.3 -> x = x - 0.3
        # x = x + 0.3
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('audio/laser.wav')
                    bullet_Sound.play()
                    # current x coordinates of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 770:
        playerX = 770

    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 730:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('audio/explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            # score
            score_value += 1
            # respawn
            enemyX[i] = random.randint(0, 720)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()