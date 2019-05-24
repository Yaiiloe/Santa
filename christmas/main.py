#!/bin/python3
import pygame, sys
import pygame.freetype
import random

pygame.init()
size = WIDTH, HEIGHT = 500, 500
BLACK = 0, 0, 0
WHITE = 255, 255, 255
# fps = 300
# fclock = pygame.time.Clock()
score = 0
pressed = None
screen = pygame.display.set_mode(size, 0, 32)
icon = pygame.image.load("gift1.png")
pygame.display.set_icon(icon)
pygame.display.set_caption('Santa Game')

# font = pygame.font.SysFont('Lato', 24)
font = pygame.freetype.Font("C://Windows//Fonts//msyh.ttc", 24)

# Load the sound effects
catch_sound = pygame.mixer.Sound("car_door.wav")
bgm = "bgm.mp3"
if pygame.mixer:
    pygame.mixer.music.load(bgm)
    pygame.mixer.music.play(-1)

# Load game character
santa = pygame.image.load('santa.png')
SANTA_WIDTH, SANTA_HEIGHT = santa.get_size()
# santa_rect = santa.get_rect() #
# print(santa_rect.x, santa_rect.y) #
# Resize santa
santa = pygame.transform.scale(santa, (SANTA_WIDTH // 2, SANTA_HEIGHT // 2))
# Set santa's initial position: center left edge of the screen
santa_y = HEIGHT / 2 - santa.get_rect().height / 2

# Load game props
gift_images = [pygame.image.load('gift1.png'), pygame.image.load('gift2.png')]
# Resize gift_images
gift_images = [pygame.transform.scale(gift, (gift.get_width() // 2, gift.get_height() // 2)) for gift in gift_images]
GIFT_SPEED = 0.3
gift_index = 0
# Define gifts:
#   gift start position(outside the right edge of the window): gift[0]
#   gift1 or gift2: gift[1]
#   gift x-speed: gift[2]
gifts = []
for i in range(5):
    gift_style = random.choice(gift_images)
    gifts.append([[WIDTH, random.randint(0, HEIGHT - gift_style.get_rect().height)], gift_style, GIFT_SPEED])

# Define snowflakes with circle-draw:
#   pos: snowflakes[0]
#   radius: snowflakes[1]
snowflakes = []
for i in range(30):
    snowflakes.append([[random.randint(0, WIDTH), random.randint(0, HEIGHT)], random.randint(2, 8)])

while True:
    screen.fill(BLACK)
    for snowflake in snowflakes:
        pygame.draw.circle(screen, WHITE, snowflake[0], snowflake[1])
        snowflake[0][1] += 1
        if snowflake[0][1] > HEIGHT + snowflake[1]:
            snowflake[0][1] = 0 - snowflake[1]

    screen.blit(santa, (0, santa_y))
    santa_rect = santa.get_rect()
    santa_rect.x = 0
    santa_rect.y = santa_y

    gift = gifts[gift_index]
    screen.blit(gift[1], gift[0])
    gift_rect = gift[1].get_rect()
    gift[0][0] -= gift[2]
    if gift[0][0] < 0 - gift_rect.width:
        score -= 1
        gift[0][0] = WIDTH
        gift[0][1] = random.randint(0, HEIGHT - gift_rect.height)
        if gift_index < len(gifts) - 1:
            gift_index += 1
        else:
            gift_index = 0

    gift_rect.x = gift[0][0]
    gift_rect.y = gift[0][1]

    if santa_rect.colliderect(gift_rect):
        catch_sound.play()
        score += 1
        gift[2] += 0.04
        gift[0][0] = WIDTH
        gift[0][1] = random.randint(0, HEIGHT - gift_rect.height)
        if gift_index < len(gifts) - 1:
            gift_index += 1
        else:
            gift_index = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            # pygame.quit()
        elif event.type == pygame.KEYDOWN:
            pressed = event.key
        elif event.type == pygame.KEYUP:
            pressed = None
    if pressed == pygame.K_UP:
        if santa_y > 0:
            santa_y -= 1
    elif pressed == pygame.K_DOWN:
        if santa_y < HEIGHT - santa_rect.height:        # Prevent gift from flying out of window range
            santa_y += 1

    score_text_surf, score_text_rect = font.render('Score: ' + str(score), fgcolor=WHITE, size=20)
    screen.blit(score_text_surf, (WIDTH / 2 - score_text_rect.width / 2, 0))        # Set score caption in the middle

    pygame.display.update()
    # fclock.tick(fps)
