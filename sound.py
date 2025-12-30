import pygame
import os

pygame.mixer.init()

sound_files = {
    "game_over": "/Volumes/DATA/pygame/Sounds/mixkit-arcade-retro-game-over-213.wav",
    "Eat": "/Volumes/DATA/pygame/Sounds/mixkit-interface-device-click-2577.wav",
    "Notification": "/Volumes/DATA/pygame/Sounds/mixkit-retro-game-notification-212.wav",
    "Exit_Button": "/Volumes/DATA/pygame/Sounds/mixkit-interface-option-select-2573.wav",
    "Start_Menu": "/Volumes/DATA/pygame/Sounds/mixkit-game-level-music-689 (1).wav",
    "Start Game": "/Volumes/DATA/pygame/Sounds/mixkit-play-bling-achievement-2067.wav",
    
}

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        for name, path in sound_files.items():
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)
            else:
                print(f"⚠️ Sound file not found: {path}")

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def set_volume(self, name, volume):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)

    def stop_all(self):
        pygame.mixer.stop()
