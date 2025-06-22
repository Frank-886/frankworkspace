import pygame
import time
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Game settings
DIS_WIDTH = 800
DIS_HEIGHT = 600
SNAKE_BLOCK = 20
SNAKE_SPEED = 15

# Initialize game window
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')

clock = pygame.time.Clock()

# Font styles
font_style = pygame.font.SysFont("arial", 25)
score_font = pygame.font.SysFont("arial", 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        center = (int(x[0] + snake_block // 2), int(x[1] + snake_block // 2))
        radius = snake_block // 2  # 更饱满的圆形
        pygame.draw.circle(dis, GREEN, center, radius)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [DIS_WIDTH / 6, DIS_HEIGHT / 3])

def gameLoop():
    game_over = False
    game_close = False

    # Starting position
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    # Position change
    x1_change = 0
    y1_change = 0

    # Snake body
    snake_list = []
    length_of_snake = 1

    # Food position
    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0

    while not game_over:

        while game_close == True:
            dis.fill(BLUE)
            message("游戏结束! 按Q退出或C重新开始", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Check boundary collision
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True

        # Update position
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)
        
        # Draw food (now as circle)
        food_center = (int(foodx + SNAKE_BLOCK // 2), int(foody + SNAKE_BLOCK // 2))
        pygame.draw.circle(dis, RED, food_center, SNAKE_BLOCK // 2)
        
        # Update snake
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        
        # Remove extra segments
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check self collision
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(SNAKE_BLOCK, snake_list)
        
        # Update display
        pygame.display.update()

        # Check food collision
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

gameLoop()