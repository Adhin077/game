import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 40)

# Bird settings
bird_x = 50
bird_y = 300
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump_strength = -8

# Pipes
pipe_width = 70
pipe_gap = 150
pipe_speed = 4
pipes = []

# Score
score = 0

def create_pipe():
    y = random.randint(150, 450)
    top_rect = pygame.Rect(WIDTH, 0, pipe_width, y - pipe_gap // 2)
    bottom_rect = pygame.Rect(WIDTH, y + pipe_gap // 2, pipe_width, HEIGHT)
    return top_rect, bottom_rect

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    label = font.render(text, True, WHITE)
    screen.blit(label, (x + w/2 - label.get_width()/2, y + h/2 - label.get_height()/2))
    return False

def start_screen():
    while True:
        screen.fill(BLUE)
        title = font.render("Flappy Bird", True, WHITE)
        screen.blit(title, (WIDTH/2 - title.get_width()/2, 150))

        if draw_button("Start", 150, 300, 100, 50, GREEN, DARK_GREEN):
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        pygame.display.flip()
        clock.tick(30)

def game_over_screen(final_score):
    while True:
        screen.fill(BLUE)
        over_text = font.render("Game Over", True, WHITE)
        screen.blit(over_text, (WIDTH/2 - over_text.get_width()/2, 150))

        score_text = font.render(f"Score: {final_score}", True, WHITE)
        screen.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 220))

        if draw_button("Retry", 150, 300, 100, 50, GREEN, DARK_GREEN):
            return  # retry game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(30)

def game_loop():
    global bird_y, bird_velocity, pipes, score

    # Reset game state
    bird_y = 300
    bird_velocity = 0
    pipes = [create_pipe()]
    score = 0

    # Message settings
    message = "gandu"
    message_timer = 0

    while True:
        screen.fill(BLUE)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = jump_strength
                message = "gandu!"      # word shown
                message_timer = 30     # show ~0.5 sec

        # Bird physics
        bird_velocity += gravity
        bird_y += bird_velocity

        # Draw bird
        pygame.draw.circle(screen, WHITE, (bird_x, int(bird_y)), bird_radius)

        # Show message near bird
        if message_timer > 0:
            msg_text = font.render(message, True, WHITE)
            screen.blit(msg_text, (bird_x + 30, int(bird_y) - 20))
            message_timer -= 1

        # Pipes logic
        new_pipes = []
        for top, bottom in pipes:
            top.x -= pipe_speed
            bottom.x -= pipe_speed

            # Draw pipes
            pygame.draw.rect(screen, GREEN, top)
            pygame.draw.rect(screen, GREEN, bottom)

            # Scoring
            if top.x + pipe_width == bird_x:
                score += 1

            if top.right > 0:
                new_pipes.append((top, bottom))
            else:
                new_pipes.append(create_pipe())

            # Collision check
            if top.collidepoint(bird_x, bird_y) or bottom.collidepoint(bird_x, bird_y):
                game_over_screen(score)
                return

        pipes = new_pipes

        # Floor/ceiling collision
        if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT:
            game_over_screen(score)
            return

        # Score display
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()
        clock.tick(60)

# Run game
start_screen()
while True:
    game_loop()
