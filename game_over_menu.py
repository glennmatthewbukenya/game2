import pygame
import sys
from sound import SoundManager

sound = SoundManager()

# ---------------- LOADING SCREEN (≈ 1 SECOND TOTAL) ----------------
def loading_overlay(screen, WIDTH, HEIGHT):
    clock = pygame.time.Clock()

    # Loading bar config
    num_bars = 2
    bar_width = 180
    bar_height = 25
    spacing = 50
    start_x = WIDTH // 2 - (num_bars * (bar_width + spacing)) // 2
    y = HEIGHT // 2 + 220

    # Background crack image
    crack_img = pygame.image.load(
        "/Volumes/DATA/pygame/assets/gameover-wall-crack.jpg"
    ).convert()
    crack_img = pygame.transform.scale(crack_img, (WIDTH, HEIGHT))

    for i in range(num_bars):
        # Fade-in animation
        for alpha in range(0, 256, 15):
            screen.blit(crack_img, (0, 0))

            for j in range(i + 1):
                rect_x = start_x + j * (bar_width + spacing)
                bar_surface = pygame.Surface((bar_width, bar_height))
                bar_surface.set_alpha(alpha)
                bar_surface.fill((120, 80, 255))
                screen.blit(bar_surface, (rect_x, y))

            pygame.display.update()
            clock.tick(60)

        # Reduced delay for ~1 second total load
        pygame.time.delay(20)

# ---------------- GAME OVER MENU ----------------
def game_over_menu(screen, WIDTH, HEIGHT, font, total_score, food_count):

    # Background
    BG = pygame.image.load(
        "/Volumes/DATA/pygame/assets/img end.png"
    ).convert()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(120)
    overlay.fill((0, 0, 0))

    # Buttons
    start_btn = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 - 20, 240, 60)
    menu_btn = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 60, 240, 60)
    exit_btn = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 140, 240, 60)

    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))
        screen.blit(overlay, (0, 0))

        # Title & Scores
        screen.blit(
            font.render("GAME OVER", True, (255, 80, 80)),
            (WIDTH // 2 - 90, HEIGHT // 2 - 160),
        )
        screen.blit(
            font.render(f"TOTAL SCORE: {total_score}", True, (255, 255, 255)),
            (WIDTH // 2 - 110, HEIGHT // 2 - 120),
        )
        screen.blit(
            font.render(f"FOOD EATEN: {food_count}", True, (255, 255, 255)),
            (WIDTH // 2 - 110, HEIGHT // 2 - 90),
        )

        # Hover color helper
        def hover(rect, color):
            return tuple(min(c + 60, 255) for c in color) if rect.collidepoint(mouse_pos) else color

        start_color = hover(start_btn, (120, 80, 255))
        menu_color = hover(menu_btn, (255, 200, 60))
        exit_color = hover(exit_btn, (0, 0, 0))

        # Start Again
        pygame.draw.rect(screen, start_color, start_btn, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), start_btn, 3, border_radius=12)
        screen.blit(
            font.render("START AGAIN", True, (255, 255, 255)),
            (start_btn.x + 60, start_btn.y + 18),
        )

        # Main Menu
        pygame.draw.rect(screen, menu_color, menu_btn, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), menu_btn, 3, border_radius=12)
        screen.blit(
            font.render("MAIN MENU", True, (0, 0, 0)),
            (menu_btn.x + 70, menu_btn.y + 18),
        )

        # Exit
        pygame.draw.rect(screen, exit_color, exit_btn, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), exit_btn, 3, border_radius=12)
        screen.blit(
            font.render("EXIT", True, (255, 255, 255)),
            (exit_btn.x + 105, exit_btn.y + 18),
        )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound.play("Exit_Button")
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    sound.play("Notification")
                    loading_overlay(screen, WIDTH, HEIGHT)
                    return "restart"

                elif menu_btn.collidepoint(event.pos):
                    sound.play("Notification")
                    loading_overlay(screen, WIDTH, HEIGHT)
                    return "menu"

                elif exit_btn.collidepoint(event.pos):
                    sound.play("Exit_Button")
                    loading_overlay(screen, WIDTH, HEIGHT)
                    pygame.quit()
                    sys.exit()

        clock.tick(60)
