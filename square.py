import pygame
import numpy as np
import random

# Constants
GRID_SIZE = 30
WIDTH, HEIGHT = 400, 400
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
FPS = 30
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Pixel class
class Pixel:
    def __init__(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)

    def move(self, dx, dy):
        self.x = max(0, min(GRID_WIDTH - 1, self.x + dx))
        self.y = max(0, min(GRID_HEIGHT - 1, self.y + dy))

    def draw(self, color):
        pygame.draw.rect(screen, color, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Q-Learning parameters
num_actions = 4  # Up, Down, Left, Right
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.1

# Initialize Q-table
q_table = np.zeros((GRID_WIDTH, GRID_HEIGHT, num_actions))

# Auto-restart parameters
max_generations = 1000
generation = 1

# Game loop
done = False

while generation <= max_generations:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Create a new pixel at the beginning of each generation
    pixel = Pixel()
    
    # Randomly choose the initial action for this generation
    initial_action = random.randint(0, num_actions - 1)

    while not done:
        # Convert pixel position to grid position
        x_grid, y_grid = pixel.x, pixel.y

        # Choose an action using epsilon-greedy policy
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, num_actions - 1)
        else:
            action = np.argmax(q_table[x_grid, y_grid, :])

        # Execute the chosen action
        if action == 0:
            pixel.move(0, -1)  # Up
        elif action == 1:
            pixel.move(0, 1)  # Down
        elif action == 2:
            pixel.move(-1, 0)  # Left
        elif action == 3:
            pixel.move(1, 0)  # Right

        # Check if the pixel has reached the red pixel
        if (pixel.x, pixel.y) == (GRID_WIDTH // 2, GRID_HEIGHT // 2):
            reward = 1
            done = True
        # Check if the pixel has touched the edge
        elif pixel.x == 0 or pixel.x == GRID_WIDTH - 1 or pixel.y == 0 or pixel.y == GRID_HEIGHT - 1:
            reward = -1
            done = True
        else:
            reward = 0

        # Update Q-value using Q-learning
        x_grid_next, y_grid_next = pixel.x, pixel.y
        q_table[x_grid, y_grid, action] = (1 - learning_rate) * q_table[x_grid, y_grid, action] + \
                                          learning_rate * (reward + discount_factor * np.max(q_table[x_grid_next, y_grid_next, :]))

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw pixels
        pixel.draw(GREEN)
        pygame.draw.rect(screen, RED, (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw generation number
        font = pygame.font.Font(None, 36)
        text = font.render(f"Generation: {generation}/{max_generations}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Auto-restart after a certain time (e.g., 2 seconds)
    pygame.time.wait(2000)  # Pause for 2 seconds before the next generation
    done = False
    generation += 1

# Quit Pygame
pygame.quit()

