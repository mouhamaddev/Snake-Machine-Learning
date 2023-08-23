import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 30
GRID_WIDTH = 13
GRID_HEIGHT = 9
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT
SNAKE_SPEED = 7  # Increase for faster gameplay

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Direction
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize the snake and apple positions
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = RIGHT
apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

game_over = False

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != DOWN:
                snake_direction = UP
            elif event.key == pygame.K_DOWN and snake_direction != UP:
                snake_direction = DOWN
            elif event.key == pygame.K_LEFT and snake_direction != RIGHT:
                snake_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake_direction != LEFT:
                snake_direction = RIGHT
            elif event.key == pygame.K_r:
                # Restart the game if 'R' is pressed
                snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                snake_direction = RIGHT
                apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                game_over = False

    if not game_over:
        # Move the snake
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        # Calculate vision points
        head_x, head_y = snake[0]
        vision_ahead = (head_x + 3 * snake_direction[0], head_y + 3 * snake_direction[1])  # Three grid units ahead
        vision_left = (head_x + 3 * snake_direction[1], head_y - 3 * snake_direction[0])    # Three grid units to the left
        vision_right = (head_x - 3 * snake_direction[1], head_y + 3 * snake_direction[0])   # Three grid units to the right

        # Calculate diagonal lines
        diagonal_top_left = (head_x - 3, head_y - 3)
        diagonal_bottom_right = (head_x + 3, head_y + 3)

        # Check for collisions
        if snake[0] == apple:
            apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        else:
            snake.pop()

        # Check if the snake collided with itself or the walls
        if (
            snake[0] in snake[1:]
            or snake[0][0] < 0
            or snake[0][0] >= GRID_WIDTH
            or snake[0][1] < 0
            or snake[0][1] >= GRID_HEIGHT
        ):
            game_over = True

    # Draw everything
    screen.fill(BLACK)

    # Draw the blue vision lines
    # Draw the vision lines as blue lines
    pygame.draw.line(screen, BLUE, (head_x * GRID_SIZE + GRID_SIZE // 2, head_y * GRID_SIZE + GRID_SIZE // 2),
                     (vision_ahead[0] * GRID_SIZE + GRID_SIZE // 2, vision_ahead[1] * GRID_SIZE + GRID_SIZE // 2), 3)
    pygame.draw.line(screen, BLUE, (head_x * GRID_SIZE + GRID_SIZE // 2, head_y * GRID_SIZE + GRID_SIZE // 2),
                     (vision_left[0] * GRID_SIZE + GRID_SIZE // 2, vision_left[1] * GRID_SIZE + GRID_SIZE // 2), 3)
    pygame.draw.line(screen, BLUE, (head_x * GRID_SIZE + GRID_SIZE // 2, head_y * GRID_SIZE + GRID_SIZE // 2),
                     (vision_right[0] * GRID_SIZE + GRID_SIZE // 2, vision_right[1] * GRID_SIZE + GRID_SIZE // 2), 3)

    # Draw the diagonal lines
    pygame.draw.line(screen, BLUE, (head_x * GRID_SIZE + GRID_SIZE // 2, head_y * GRID_SIZE + GRID_SIZE // 2),
                     (diagonal_top_left[0] * GRID_SIZE + GRID_SIZE // 2, diagonal_top_left[1] * GRID_SIZE + GRID_SIZE // 2), 3)
    pygame.draw.line(screen, BLUE, (head_x * GRID_SIZE + GRID_SIZE // 2, head_y * GRID_SIZE + GRID_SIZE // 2),
                     (diagonal_bottom_right[0] * GRID_SIZE + GRID_SIZE // 2, diagonal_bottom_right[1] * GRID_SIZE + GRID_SIZE // 2), 3)
    
    # Draw the diagonal lines you wanted
    diagonal_top_right = (head_x + 3, head_y - 3)
    diagonal_bottom_left = (head_x - 3, head_y + 3)
    pygame.draw.line(screen, BLUE, (head_x * GRID_SIZE + GRID_SIZE // 2, head_y * GRID_SIZE + GRID_SIZE // 2),
                     (diagonal_top_right[0] * GRID_SIZE + GRID_SIZE // 2, diagonal_top_right[1] * GRID_SIZE + GRID_SIZE // 2), 3)
    pygame.draw.line(screen, BLUE, (head_x * GRID_SIZE + GRID_SIZE // 2, head_y * GRID_SIZE + GRID_SIZE // 2),
                     (diagonal_bottom_left[0] * GRID_SIZE + GRID_SIZE // 2, diagonal_bottom_left[1] * GRID_SIZE + GRID_SIZE // 2), 3)

    # Draw the snake and apple
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, RED, (apple[0] * GRID_SIZE, apple[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    if game_over:
        snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        snake_direction = RIGHT
        apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        game_over = False

    pygame.display.update()

    # Control game speed
    clock.tick(SNAKE_SPEED)
