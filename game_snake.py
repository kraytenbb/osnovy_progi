import pygame
import random
import sys

pygame.init()

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 6

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка с текстурами и поворачивающейся головой")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

background_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
snake_head_img = pygame.image.load("snake_head.png").convert_alpha()
snake_head_img = pygame.transform.scale(snake_head_img, (CELL_SIZE, CELL_SIZE))
snake_body_img = pygame.image.load("snake_body.png").convert_alpha()
snake_body_img = pygame.transform.scale(snake_body_img, (CELL_SIZE, CELL_SIZE))
apple_img = pygame.image.load("apple.png").convert_alpha()
apple_img = pygame.transform.scale(apple_img, (CELL_SIZE, CELL_SIZE))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTION_TO_ANGLE = {
    RIGHT: 0,
    DOWN: -90,
    LEFT: 180,
    UP: 90
}


def draw_background():
    screen.blit(background_img, (0, 0))


def draw_cell_with_texture(position, img):
    x = position[0] * CELL_SIZE
    y = position[1] * CELL_SIZE
    screen.blit(img, (x, y))


def random_food_position(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos


def game_over_screen(score):
    screen.fill(BLACK)
    msg1 = font.render(f"Игра окончена! Счёт: {score}", True, RED)
    msg2 = font.render("Нажмите любую клавишу для перезапуска", True, WHITE)
    screen.blit(msg1, (WIDTH//2 - msg1.get_width()//2, HEIGHT//3))
    screen.blit(msg2, (WIDTH//2 - msg2.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(500)
    wait_for_key()


def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return


def main():
    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
    direction = RIGHT
    food = random_food_position(snake)
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if (
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in snake
        ):
            game_over_screen(score)
            return main()

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = random_food_position(snake)
        else:
            snake.pop()

        draw_background()
        angle = DIRECTION_TO_ANGLE[direction]
        rotated_head = pygame.transform.rotate(snake_head_img, angle)
        head_x = snake[0][0] * CELL_SIZE
        head_y = snake[0][1] * CELL_SIZE
        head_rect = rotated_head.get_rect(center=(head_x + CELL_SIZE//2, head_y + CELL_SIZE//2))
        screen.blit(rotated_head, head_rect.topleft)
        for segment in snake[1:]:
            draw_cell_with_texture(segment, snake_body_img)
        draw_cell_with_texture(food, apple_img)

        score_text = font.render(f"Счёт: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
