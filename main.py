import pygame
import sys
import time
import math
from sound import SoundManager
from start_menu import start_menu
from game_over_menu import game_over_menu
from snake import Snake
from food import Food

pygame.init()
pygame.mixer.init()

# ---------------- SOUND ----------------
sound = SoundManager()
sound.set_volume("Eat", 0.6)
sound.set_volume("game_over", 0.8)
sound.set_volume("Notification", 0.5)
sound.set_volume("Exit_Button", 0.5)

def play_sound(name):
    try:
        sound.play(name)
    except:
        pass

# ---------------- SCREEN & CONSTANTS ----------------
WIDTH, HEIGHT = 1110, 550
NAVBAR_HEIGHT = 50
snake_size = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont("arial", 18)
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GRAY = (30, 30, 30)
WHITE = (255, 255, 255)

# ---------------- BACKGROUND ----------------
GAMEPLAY_BG_PATH = "/Volumes/DATA/pygame/assets/gameplay2.png"
gameplay_bg = pygame.image.load(GAMEPLAY_BG_PATH).convert()
gameplay_bg = pygame.transform.scale(gameplay_bg, (WIDTH, HEIGHT - NAVBAR_HEIGHT))

# ---------------- UI HELPERS ----------------
def draw_text(text, x, y, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))

def draw_navbar(level, mode, score, elapsed):
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, NAVBAR_HEIGHT))
    draw_text(f"LEVEL: {level}", 20, 10)
    draw_text(f"MODE: {mode}", 180, 10)
    draw_text(f"SCORE: {score}", 350, 10)
    draw_text(f"TIME: {elapsed:.1f}s", 520, 10)

# ---------------- GAME LOOP ----------------
def game_loop(FPS, MODE):
    snake = Snake(
        start_pos=[120, NAVBAR_HEIGHT + 30],
        size=snake_size,
        navbar_height=NAVBAR_HEIGHT
    )

    food = Food(WIDTH, HEIGHT, snake_size, NAVBAR_HEIGHT)

    start_time = time.time()
    score = 0
    food_eaten = 0

    wigwag_amplitude = 4
    wigwag_speed = 5

    while True:
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play_sound("Exit_Button")
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")

        snake.move()

        if food.eaten(snake.pos):
            play_sound("Eat")
            score += FPS ** 2
            food_eaten += 1
            food.respawn(snake.body)
            snake.grow()
        else:
            snake.shrink()

        if snake.hit_wall(WIDTH, HEIGHT) or snake.hit_self():
            play_sound("game_over")
            return game_over_menu(screen, WIDTH, HEIGHT, font, score, food_eaten)

        # ---------------- DRAW ----------------
        screen.fill(BLACK)
        screen.blit(gameplay_bg, (0, NAVBAR_HEIGHT))
        draw_navbar(FPS, MODE, score, elapsed_time)

        for block in snake.body:
            pygame.draw.rect(screen, GREEN, (*block, snake_size, snake_size))

        wigwag = wigwag_amplitude * math.sin(elapsed_time * wigwag_speed)
        food_pos = (int(food.position[0] + wigwag), food.position[1])
        pygame.draw.rect(screen, RED, (*food_pos, snake_size, snake_size))

        pygame.display.update()
        clock.tick(FPS)

# ---------------- MAIN ----------------
def main():
    while True:
        fps, mode, *_ = start_menu(screen, WIDTH, HEIGHT, font, game_loop)
        if fps is None:
            pygame.quit()
            sys.exit()

        result = game_loop(fps, mode)
        if result in ("menu", "restart"):
            continue

if __name__ == "__main__":
    main()
