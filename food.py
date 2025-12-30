# Food spawning & collision detection module
import random

class Food:
    def __init__(self, width, height, size, navbar_height):
        self.width = width
        self.height = height
        self.size = size
        self.navbar_height = navbar_height
        self.position = self.spawn()

    def spawn(self):
        return [
            random.randrange(0, self.width - self.size, self.size),
            random.randrange(self.navbar_height, self.height - self.size, self.size),
        ]

    def respawn(self, snake_body):
        while True:
            pos = self.spawn()
            if pos not in snake_body:
                self.position = pos
                return

    def eaten(self, snake_pos):
        return snake_pos == self.position
