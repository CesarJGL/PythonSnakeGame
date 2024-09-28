import pygame
import random

pygame.init()
square_width = 750
pixel_width = 50
screen = pygame.display.set_mode([square_width] * 2)
clock = pygame.time.Clock()
running = True

# Initialize the score
score = 0
font = pygame.font.Font(None, 36)
paused = False  # Track if the game is paused

# Instruction commands
instruction_texts = [
    "Use arrow keys to move",
    "Press 'P' to pause",
]

def generate_starting_position():
    position_range = (pixel_width // 2, square_width - pixel_width // 2, pixel_width)
    return [random.randrange(*position_range), random.randrange(*position_range)]

def reset():
    global score, snake_length, snake, snake_direction
    score = 0
    snake_length = 1
    snake_direction = (0, 0)  # Reset direction
    snake = [snake_pixel.copy()]
    target.center = generate_starting_position()
    snake_pixel.center = generate_starting_position()

def handle_screen_wrap():
    if snake_pixel.left < 0:
        snake_pixel.right = square_width
    elif snake_pixel.right > square_width:
        snake_pixel.left = 0
    elif snake_pixel.top < 0:
        snake_pixel.bottom = square_width
    elif snake_pixel.bottom > square_width:
        snake_pixel.top = 0

def display_welcome_message():
    welcome_text = font.render("Welcome to my Python Snake Game!", True, (255, 255, 255))
    instructions_text = font.render("Press an arrow key to begin", True, (255, 255, 255))

    screen.fill("black")
    screen.blit(welcome_text, (square_width // 2 - welcome_text.get_width() // 2, square_width // 2 - 40))
    screen.blit(instructions_text, (square_width // 2 - instructions_text.get_width() // 2, square_width // 2))

    pygame.display.flip()

def display_game_over_message():
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))  # Display the score
    restart_text = font.render("Press an arrow key to play again", True, (255, 255, 255))
    quit_text = font.render("Quit Game", True, (255, 255, 255))  # Quit button text

    button_width = 200
    button_height = 50
    quit_button_rect = pygame.Rect(
        (square_width // 2 - button_width // 2, square_width // 2 + 40, button_width, button_height))

    screen.fill("black")
    screen.blit(game_over_text, (square_width // 2 - game_over_text.get_width() // 2, square_width // 2 - 80))
    screen.blit(score_text, (square_width // 2 - score_text.get_width() // 2, square_width // 2 - 40))  # Center the score text
    screen.blit(restart_text, (square_width // 2 - restart_text.get_width() // 2, square_width // 2))

    # Draw the quit button rectangle
    pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)  # Draw button in red
    screen.blit(quit_text, (quit_button_rect.x + (quit_button_rect.width // 2 - quit_text.get_width() // 2),
                             quit_button_rect.y + (quit_button_rect.height // 2 - quit_text.get_height() // 2)))  # Center text in button

    pygame.display.flip()

    return quit_button_rect

snake_pixel = pygame.Rect([0, 0, pixel_width - 2, pixel_width - 2])
snake_pixel.center = generate_starting_position()
snake = [snake_pixel.copy()]
snake_direction = (0, 0)
snake_length = 1

target = pygame.Rect([0, 0, pixel_width - 2, pixel_width - 2])
target.center = generate_starting_position()

# Display the welcome message
display_welcome_message()

# Wait for an arrow key press to start the game
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                waiting = False  # Start the game

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Toggle pause with 'P'
                paused = not paused

    if paused:
        pause_text = font.render("Paused. Press 'P' to continue.", True, (255, 255, 255))
        screen.fill("black")
        screen.blit(pause_text, (square_width // 2 - pause_text.get_width() // 2, square_width // 2 - 20))
        pygame.display.flip()
        continue

    screen.fill("black")

    # Check for border wrapping
    handle_screen_wrap()

    # Check for collision with the target
    if snake_pixel.colliderect(target):
        target.center = generate_starting_position()
        snake_length += 1
        snake.append(snake_pixel.copy())
        # Increase the score
        score += 1

    # Handle snake movement based on arrow keys
    keys = pygame.key.get_pressed()
    new_direction = snake_direction

    if keys[pygame.K_UP]:
        new_direction = (0, -pixel_width)
    if keys[pygame.K_DOWN]:
        new_direction = (0, pixel_width)
    if keys[pygame.K_LEFT]:
        new_direction = (-pixel_width, 0)
    if keys[pygame.K_RIGHT]:
        new_direction = (pixel_width, 0)

    # Prevent the snake from moving in the opposite direction
    if (new_direction[0] * -1, new_direction[1] * -1) != snake_direction:
        snake_direction = new_direction

    # Move the snake and check for self-collision
    snake_pixel.move_ip(snake_direction)
    snake.append(snake_pixel.copy())

    # Check for self-collision
    if snake_pixel in snake[:-1]:  # Check if the snake's head is in the body
        quit_button_rect = display_game_over_message()  # Show Game Over message
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        reset()  # Reset the game if an arrow key is pressed
                        waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = event.pos
                        if quit_button_rect.collidepoint(mouse_pos):  # Check if the mouse clicks the quit button
                            running = False
                            waiting = False

    snake = snake[-snake_length:]

    # Draw the snake as solid blocks with no visible lines
    for snake_part in snake:
        pygame.draw.rect(screen, "green", snake_part.inflate(-2, -2))  # Inflate to remove separation

    # Draw the target with a random color
    target_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    pygame.draw.circle(screen, target_color, target.center, pixel_width // 2 - 2)

    # Render the score counter
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Render instruction commands
    for i, text in enumerate(instruction_texts):
        instruction_text = font.render(text, True, (255, 255, 255))
        screen.blit(instruction_text, (square_width - instruction_text.get_width() - 10, 10 + i * 20))

    pygame.display.flip()

    clock.tick(10)

pygame.quit()