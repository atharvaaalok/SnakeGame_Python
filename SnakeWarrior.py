import pygame
from pygame import mixer
import random
import time
import math

# Initialize pygame
pygame.init()

# Draw rectangle for boundary
def draw_boundary():    
    pygame.draw.rect(screen, BOUNDARY_COLOR, (0, 0 + SCORE_WIDTH, BOUNDARY_WIDTH, (HEIGHT - SCORE_WIDTH)))
    pygame.draw.rect(screen, BOUNDARY_COLOR, (0, 0 + SCORE_WIDTH, WIDTH, BOUNDARY_WIDTH))
    pygame.draw.rect(screen, BOUNDARY_COLOR, ((WIDTH - BOUNDARY_WIDTH), 0 + SCORE_WIDTH, BOUNDARY_WIDTH, (HEIGHT - SCORE_WIDTH)))
    pygame.draw.rect(screen, BOUNDARY_COLOR, (0, (HEIGHT - BOUNDARY_WIDTH), WIDTH, BOUNDARY_WIDTH))


# Display score
def score_display():
    pygame.draw.rect(screen, SCORE_BOUNDARY_COLOR, (0, 0, WIDTH, SCORE_WIDTH))
    score_value = font.render("SCORE : " + str(score), True, SCORE_COLOR)
    screen.blit(score_value, (10, 10))

# Draw the apple at a random place
def draw_apple():
    # Draw the apple
    screen.blit(appleImg, (appleX, appleY))


# Drawing the snake
def draw_snake():
    pygame.draw.rect(screen, SNAKE_COLOR, (SNAKE_COORDINATES_X[0], SNAKE_COORDINATES_Y[0], SNAKE_WIDTH, SNAKE_WIDTH))
    center1 = (SNAKE_COORDINATES_X[0] + 7, SNAKE_COORDINATES_Y[0] + 6)
    center2 = (SNAKE_COORDINATES_X[0] + 14, SNAKE_COORDINATES_Y[0] + 6)
    pygame.draw.circle(screen, SNAKE_EYE_COLOR, center1, SNAKE_EYE_RADIUS)
    pygame.draw.circle(screen, SNAKE_EYE_COLOR, center2, SNAKE_EYE_RADIUS)
    for i in range(SNAKE_LENGTH - 1):
        pygame.draw.rect(screen, SNAKE_COLOR, (SNAKE_COORDINATES_X[i + 1], SNAKE_COORDINATES_Y[i + 1], SNAKE_WIDTH, SNAKE_WIDTH))


# Snake eats the apple generate new apple
def eat_apple():
    global appleX, appleY, SNAKE_COORDINATES_X, SNAKE_COORDINATES_Y, SNAKE_LENGTH, score
    # dist = math.sqrt(pow((appleX - SNAKE_COORDINATES_X[0]), 2) + pow((appleY - SNAKE_COORDINATES_Y[0]), 2))
    if appleX == SNAKE_COORDINATES_X[0] and appleY == SNAKE_COORDINATES_Y[0]:
        eating_sound.play()
        appleX = random.randint((BOUNDARY_WIDTH) / 2, (WIDTH - BOUNDARY_WIDTH - APPLE_SIZE) / 20) * 20
        appleY = random.randint((BOUNDARY_WIDTH + SCORE_WIDTH) / 2, (HEIGHT - BOUNDARY_WIDTH - APPLE_SIZE) / 20) * 20
        # Increasing  the snake length on eating the apple
        SNAKE_LENGTH += 1
        score += 10
        # Appending another body part
        SNAKE_COORDINATES_X.append(SNAKE_COORDINATES_X[0])
        SNAKE_COORDINATES_Y.append(SNAKE_COORDINATES_Y[0])


# Snake head collision with boundary
def collision():
    global snakeX_change, snakeY_change, running
    if (SNAKE_COORDINATES_X[0] < (BOUNDARY_WIDTH - BOUNDARY_EXTENSION))  or ((SNAKE_COORDINATES_X[0] + SNAKE_WIDTH) > (WIDTH - BOUNDARY_WIDTH + BOUNDARY_EXTENSION)) or SNAKE_COORDINATES_Y[0] < (BOUNDARY_WIDTH + SCORE_WIDTH - BOUNDARY_EXTENSION) or ((SNAKE_COORDINATES_Y[0] + SNAKE_WIDTH) > (HEIGHT - BOUNDARY_WIDTH + BOUNDARY_EXTENSION)):
        explosion_sound.play()
        running = False
        snakeX_change = 0
        snakeY_change = 0
        time.sleep(1)


# Snake bites itself
def bite():
    global running, snakeX_change, snakeY_change
    for i in range(SNAKE_LENGTH - 1):
        if SNAKE_COORDINATES_X[0] == SNAKE_COORDINATES_X[i + 1] and SNAKE_COORDINATES_Y[0] == SNAKE_COORDINATES_Y[i + 1]:
            running = False
            explosion_sound.play()
            snakeX_change = 0
            snakeY_change = 0
            time.sleep(1)


def main():
    global screen, snakeX_change, snakeY_change,running

    # Game loop 
    while running:

        # Displaying the screen
        screen.fill((46, 204, 113))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # If a key is pressed 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if snakeX_change == SNAKE_SPEED:
                        pass
                    else:
                        snakeX_change = -SNAKE_SPEED
                        snakeY_change = 0
                elif event.key == pygame.K_RIGHT:
                    if snakeX_change == -SNAKE_SPEED:
                        pass
                    else:
                        snakeX_change = SNAKE_SPEED
                        snakeY_change = 0
                elif event.key == pygame.K_UP:
                    if snakeY_change == SNAKE_SPEED:
                        pass
                    else:
                        snakeY_change = -SNAKE_SPEED
                        snakeX_change = 0
                elif event.key == pygame.K_DOWN:
                    if snakeY_change == -SNAKE_SPEED:
                        pass
                    else:
                        snakeY_change = SNAKE_SPEED
                        snakeX_change = 0
                                                        

                
        pygame.time.delay(60)

        for i in range(SNAKE_LENGTH - 1, 0, -1):
            SNAKE_COORDINATES_X[i] = SNAKE_COORDINATES_X[i - 1]
            SNAKE_COORDINATES_Y[i] = SNAKE_COORDINATES_Y[i - 1]
        
        SNAKE_COORDINATES_X[0] += snakeX_change
        SNAKE_COORDINATES_Y[0] += snakeY_change
        
        collision()
        bite()
        eat_apple()
        draw_boundary()
        score_display()
        draw_apple()
        draw_snake()
        #clock.tick(60)
        pygame.display.update()


running = True
# Screen specifications
HEIGHT = 800
WIDTH = 800

# Score details
SCORE_WIDTH = 40
SCORE_FONT = 0
SCORE_SIZE = 25
SCORE_COLOR = (74, 35, 90)
SCORE_BOUNDARY_COLOR = (244, 208, 63)
score = 0
font = pygame.font.Font('Bubblegum.ttf', SCORE_SIZE)

# Boundary details
BOUNDARY_COLOR = (44, 62, 80)
BOUNDARY_WIDTH = 20
BOUNDARY_EXTENSION = 1

# Snake features
SNAKE_COLOR = (211, 84, 0)
SNAKE_EYE_COLOR = (255, 255, 255)
SNAKE_EYE_RADIUS = 2
SNAKE_WIDTH = 20
SNAKE_LENGTH = 1
snakeX_initial = 400
snakeY_initial = 400
snakeX_change = 0
snakeY_change = 0
SNAKE_SPEED = SNAKE_WIDTH
SNAKE_COORDINATES_X = [snakeX_initial]
SNAKE_COORDINATES_Y = [snakeY_initial]
SNAKE_BODY_LAG = 20



# Clock
clock =  pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and Icon
pygame.display.set_caption('Snake Warrior')
icon = pygame.image.load('pythoniconSmall.png')
pygame.display.set_icon(icon)

# Background Sound
mixer.music.load('believer-wav.wav')
mixer.music.play(-1)

# Eating sound and Explosion sound
eating_sound = mixer.Sound('apple-crunch-wav.wav')
explosion_sound = mixer.Sound('explosion-wav.wav')


# Apple
APPLE_SIZE = 20
appleImg = pygame.image.load('appleSmall.png')
appleX = 200
appleY = 200









# Play again 
def play():
    global running
    main()
    value = input("to play again press 1")
    #    for event in pygame.event.get():
    #        # If SPACE is pressed 
    #        if event.type == pygame.KEYDOWN:
    #            if event.key == pygame.K_SPACE:
    if value == 1:
        running = True
        play()

if __name__ == '__main__':
    play()

