import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# 定义游戏参数
WIDTH = 640
HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

# 设置显示窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')

# 定义蛇类
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        cur = self.get_head_position()
        x, y = cur

        if self.direction == pygame.K_UP:
            y -= GRID_SIZE
        elif self.direction == pygame.K_DOWN:
            y += GRID_SIZE
        elif self.direction == pygame.K_LEFT:
            x -= GRID_SIZE
        elif self.direction == pygame.K_RIGHT:
            x += GRID_SIZE

        if x < 0:
            x = WIDTH - GRID_SIZE
        elif x >= WIDTH:
            x = 0
        if y < 0:
            y = HEIGHT - GRID_SIZE
        elif y >= HEIGHT:
            y = 0

        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != pygame.K_DOWN:
                    self.direction = pygame.K_UP
                elif event.key == pygame.K_DOWN and self.direction != pygame.K_UP:
                    self.direction = pygame.K_DOWN
                elif event.key == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
                    self.direction = pygame.K_LEFT
                elif event.key == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
                    self.direction = pygame.K_RIGHT

# 定义食物类
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# 主游戏函数
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        snake.handle_keys()
        snake.move()
        
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        
        score_text = font.render(f'得分: {score}', True, WHITE)
        screen.blit(score_text, (5, 5))
        
        pygame.display.update()
        
        # 检查是否撞到自己
        if snake.get_head_position() in snake.positions[1:]:
            game_over_text = font.render('游戏结束!', True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2 - 18))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

        clock.tick(SNAKE_SPEED)

if __name__ == '__main__':
    main()
