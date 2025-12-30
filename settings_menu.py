import pygame
from sound import SoundManager

pygame.init()
sound = SoundManager()

# ---------------- DEFAULT SETTINGS ----------------
DEFAULT_SETTINGS = {
    "volume": 0.6,
    "vibration": True,
    "food_color": "red",   # DEFAULT
}

FOOD_COLORS = {
    "red": (255, 0, 0),
    "gold": (255, 200, 60),
    "blue": (80, 160, 255),
    "purple": (180, 90, 255),
}

# ---------------- HELPERS ----------------
def draw_text(screen, text, x, y, font, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), (x, y))

def apply_volume(volume):
    # Music (safe even if no music loaded)
    pygame.mixer.music.set_volume(volume)

    # Sound effects (matches your SoundManager usage)
    for key in ["Eat", "game_over", "Notification", "Exit_Button"]:
        try:
            sound.set_volume(key, volume)
        except:
            pass

# ---------------- SETTINGS MENU ----------------
def settings_menu(screen, WIDTH, HEIGHT, font, settings):
    clock = pygame.time.Clock()

    volume = settings["volume"]
    vibration = settings["vibration"]
    food_color = settings["food_color"]

    slider = pygame.Rect(300, 160, 400, 8)
    checkbox = pygame.Rect(300, 230, 26, 26)

    color_buttons = {
        "gold": pygame.Rect(300, 300, 100, 40),
        "blue": pygame.Rect(420, 300, 100, 40),
        "purple": pygame.Rect(540, 300, 100, 40),
    }

    back_btn = pygame.Rect(40, HEIGHT - 80, 160, 45)
    dragging = False

    while True:
        screen.fill((15, 15, 30))

        draw_text(screen, "SETTINGS", WIDTH // 2 - 70, 40, font, (200, 180, 255))

        # -------- VOLUME --------
        draw_text(screen, "Volume", 180, 145, font)
        pygame.draw.rect(screen, (90, 90, 120), slider, border_radius=6)

        knob_x = slider.x + int(volume * slider.width)
        pygame.draw.circle(screen, (180, 120, 255), (knob_x, slider.centery), 10)

        # -------- VIBRATION --------
        draw_text(screen, "Vibration", 180, 225, font)
        pygame.draw.rect(screen, (255, 255, 255), checkbox, 2)

        if vibration:
            pygame.draw.line(screen, (120, 255, 120), checkbox.topleft, checkbox.bottomright, 3)
            pygame.draw.line(screen, (120, 255, 120), checkbox.topright, checkbox.bottomleft, 3)

        # -------- FOOD COLORS --------
        draw_text(screen, "Food Color", 180, 295, font)

        for key, rect in color_buttons.items():
            pygame.draw.rect(screen, FOOD_COLORS[key], rect, border_radius=8)
            if key == food_color:
                pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=8)

        # -------- BACK --------
        pygame.draw.rect(screen, (120, 80, 200), back_btn, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), back_btn, 2, border_radius=10)
        draw_text(screen, "BACK", back_btn.x + 50, back_btn.y + 12, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider.collidepoint(event.pos):
                    dragging = True

                if checkbox.collidepoint(event.pos):
                    vibration = not vibration
                    sound.play("Notification")

                for key, rect in color_buttons.items():
                    if rect.collidepoint(event.pos):
                        food_color = key
                        sound.play("Notification")

                if back_btn.collidepoint(event.pos):
                    apply_volume(volume)
                    return {
                        "volume": volume,
                        "vibration": vibration,
                        "food_color": food_color,
                    }

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                pos = max(slider.x, min(event.pos[0], slider.right))
                volume = (pos - slider.x) / slider.width
                apply_volume(volume)

        clock.tick(60)
