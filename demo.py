import pygame
import random
import sys

pygame.init()

# 游戏窗口大小
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('贪吃蛇小游戏')

# 颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 初始蛇和食物
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)
food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))

clock = pygame.time.Clock()

def draw_snake(snake):
    for pos in snake:
        pygame.draw.rect(screen, GREEN, (*pos, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

def move_snake(snake, direction):
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)
    return snake

def check_collision(snake):
    head = snake[0]
    # 撞墙
    if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
        return True
    # 撞自己
    if head in snake[1:]:
        return True
    return False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    snake = move_snake(snake, direction)
    # 吃到食物
    if snake[0] == food:
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
    else:
        snake.pop()

    if check_collision(snake):
        print("游戏结束！")
        pygame.quit()
        sys.exit()

    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food)
    pygame.display.flip()
    clock.tick(5)
