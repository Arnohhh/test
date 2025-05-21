import pygame
import random
import sys
import os
import json

pygame.init()
import pygame.freetype

# 排行榜文件路径
SCORE_FILE = "snake_scores.json"

# 加载排行榜
def load_scores():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 保存排行榜
def save_scores(scores):
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

# 添加分数到排行榜
def add_score(name, score):
    scores = load_scores()
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]  # 只保留前5名
    save_scores(scores)
    return scores

# 显示分数和排行榜
def draw_score_and_leaderboard(screen, score, font):
    # 当前分数
    font.render_to(screen, (10, 10), f"得分: {score}", (255, 255, 0))
    # 排行榜
    scores = load_scores()
    font.render_to(screen, (400, 10), "排行榜:", (255, 255, 255))
    for i, entry in enumerate(scores):
        font.render_to(screen, (400, 35 + i * 25), f"{i+1}. {entry['name']} {entry['score']}", (200, 200, 255))
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
