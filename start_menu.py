import pygame
from sound import SoundManager
from settings_menu import settings_menu, DEFAULT_SETTINGS

pygame.init()
sound = SoundManager()

# ---------------- TEXT HELPER ----------------
def draw_text(screen, text, x, y, font, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), (x, y))

# ----- Hover Glow Helper -----
def apply_hover_glow(rect, base_color):
    if rect.collidepoint(pygame.mouse.get_pos()):
        # brighten color slightly for glow effect
        return tuple(min(c + 60, 255) for c in base_color)
    return base_color

# ---------------- START MENU ----------------
def start_menu(screen, WIDTH, HEIGHT, font, game_loop):
    MODE = "BEGINNER"
    level = 5
    settings = DEFAULT_SETTINGS.copy()

    # Load background
    MENU_BG = pygame.image.load("/Volumes/DATA/pygame/assets/startscreen.jpg").convert()
    MENU_BG = pygame.transform.scale(MENU_BG, (WIDTH, HEIGHT))

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(120)
    overlay.fill((0, 0, 0))

    # Level boxes
    level_boxes = []
    start_x, start_y = 80, 160
    for i in range(20):
        x = start_x + (i % 10) * 50
        y = start_y + (i // 10) * 50
        level_boxes.append(pygame.Rect(x, y, 40, 40))

    # Buttons
    mode_btn = pygame.Rect(WIDTH - 220, 110, 170, 50)
    settings_btn = pygame.Rect(WIDTH - 220, 180, 170, 50)
    start_btn = pygame.Rect(WIDTH // 2 - 120, HEIGHT - 120, 240, 60)

    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(MENU_BG, (0, 0))
        screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont("arial", 42, bold=True)
        subtitle_font = pygame.font.SysFont("arial", 18)

        # Title
        draw_text(screen, "SESOTA", WIDTH // 2 - 85, 35, title_font, (190, 120, 255))
        draw_text(screen, "Celestial Snake", WIDTH // 2 - 70, 80, subtitle_font)

        # Level selection
        draw_text(screen, "Choose Level (1–20):", start_x, start_y - 40, font)
        for i, box in enumerate(level_boxes):
            box_color = apply_hover_glow(box, (60, 200, 60))
            pygame.draw.rect(screen, box_color, box, border_radius=6)
            if i + 1 == level:
                pygame.draw.rect(screen, (255, 255, 255), box, 3, border_radius=6)
            draw_text(screen, str(i + 1), box.x + 12, box.y + 8, font)

        # ----- Buttons with Hover Glow -----
        mode_color = apply_hover_glow(mode_btn, (0, 120, 255))
        pygame.draw.rect(screen, mode_color, mode_btn, border_radius=10)
        draw_text(screen, MODE, mode_btn.x + 25, mode_btn.y + 12, font)

        settings_color = apply_hover_glow(settings_btn, (120, 80, 200))
        pygame.draw.rect(screen, settings_color, settings_btn, border_radius=10)
        draw_text(screen, "SETTINGS", settings_btn.x + 35, settings_btn.y + 12, font)

        start_color = apply_hover_glow(start_btn, (100, 40, 200))
        pygame.draw.rect(screen, start_color, start_btn, border_radius=14)
        draw_text(screen, "START GAME", start_btn.x + 55, start_btn.y + 18, font)

        pygame.display.update()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Level selection
                for i, box in enumerate(level_boxes):
                    if box.collidepoint(event.pos):
                        level = i + 1

                # Toggle mode
                if mode_btn.collidepoint(event.pos):
                    MODE = "ADVANCED" if MODE == "BEGINNER" else "BEGINNER"
                    sound.play("Notification")

                # Open settings
                if settings_btn.collidepoint(event.pos):
                    settings = settings_menu(screen, WIDTH, HEIGHT, font, settings)

                # Start game
                if start_btn.collidepoint(event.pos):
                    sound.play("Start Game")

                    # ----- LOADING EFFECT -----
                    loading_font = pygame.font.SysFont("arial", 36, bold=True)
                    loading_text = loading_font.render("Loading...", True, (255, 255, 255))
                    
                    loading_overlay = pygame.Surface((WIDTH, HEIGHT))
                    loading_overlay.set_alpha(180)
                    loading_overlay.fill((0, 0, 0))
                    
                    screen.blit(loading_overlay, (0, 0))
                    screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2,
                                               HEIGHT // 2 - loading_text.get_height() // 2))
                    pygame.display.update()
                    pygame.time.delay(500)  # show for 0.5 seconds

                    return level, MODE, settings

        clock.tick(60)
