import pygame
import random
import sys
import os

pygame.init()

# 游戏窗口大小
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('贪吃蛇小游戏')

# 颜色
BLACK = (30, 30, 30)
GREEN = (0, 200, 0)
HEAD_COLOR = (0, 255, 100)
FOOD_COLORS = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 0, 255), (0, 255, 255)]
WHITE = (255, 255, 255)

# 初始蛇和食物
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)
food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
food_color = random.choice(FOOD_COLORS)

clock = pygame.time.Clock()
score = 0
FONT = pygame.font.SysFont('arial', 24)
RANK_FILE = os.path.join(os.path.dirname(__file__), 'rank.txt')

def draw_snake(snake):
    for i, pos in enumerate(snake):
        color = HEAD_COLOR if i == 0 else GREEN
        pygame.draw.rect(screen, color, (*pos, CELL_SIZE, CELL_SIZE), border_radius=6)

def draw_food(food, color):
    pygame.draw.rect(screen, color, (*food, CELL_SIZE, CELL_SIZE), border_radius=8)

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

def draw_score(score):
    score_surf = FONT.render(f"分数: {score}", True, WHITE)
    screen.blit(score_surf, (10, 10))

def save_score(score):
    try:
        with open(RANK_FILE, 'a', encoding='utf-8') as f:
            f.write(str(score) + '\n')
    except Exception:
        pass

def get_rankings():
    if not os.path.exists(RANK_FILE):
        return []
    with open(RANK_FILE, 'r', encoding='utf-8') as f:
        scores = [int(line.strip()) for line in f if line.strip().isdigit()]
    scores.sort(reverse=True)
    return scores[:5]

def show_rankings(score):
    rankings = get_rankings()
    screen.fill(BLACK)
    over_surf = FONT.render("游戏结束！", True, (255, 80, 80))
    screen.blit(over_surf, (WIDTH // 2 - over_surf.get_width() // 2, 60))
    score_surf = FONT.render(f"你的分数: {score}", True, WHITE)
    screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 110))
    rank_title = FONT.render("排行榜（前5）", True, (255, 215, 0))
    screen.blit(rank_title, (WIDTH // 2 - rank_title.get_width() // 2, 160))
    for idx, s in enumerate(rankings):
        rank_surf = FONT.render(f"{idx+1}. {s}", True, WHITE)
        screen.blit(rank_surf, (WIDTH // 2 - rank_surf.get_width() // 2, 200 + idx * 30))
    pygame.display.flip()
    pygame.time.wait(3500)

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
        score += 1
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        food_color = random.choice(FOOD_COLORS)
    else:
        snake.pop()

    if check_collision(snake):
        save_score(score)
        show_rankings(score)
        pygame.quit()
        sys.exit()

    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food, food_color)
    draw_score(score)
    pygame.display.flip()
    clock.tick(10)