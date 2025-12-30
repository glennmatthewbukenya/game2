# Snake movement, growth, self & wall collision module

class Snake:
    def __init__(self, start_pos, size, navbar_height):
        self.size = size
        self.navbar_height = navbar_height
        self.direction = "RIGHT"
        self.pos = list(start_pos)
        self.body = [list(self.pos)]

    def change_direction(self, new_direction):
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
        }
        if new_direction != opposites[self.direction]:
            self.direction = new_direction

    def move(self):
        if self.direction == "UP":
            self.pos[1] -= self.size
        elif self.direction == "DOWN":
            self.pos[1] += self.size
        elif self.direction == "LEFT":
            self.pos[0] -= self.size
        elif self.direction == "RIGHT":
            self.pos[0] += self.size

        self.body.insert(0, list(self.pos))

    def grow(self):
        
        pass

    def shrink(self):
        self.body.pop()

    def hit_wall(self, width, height):
        return (
            self.pos[0] < 0
            or self.pos[0] >= width
            or self.pos[1] < self.navbar_height
            or self.pos[1] >= height
        )

    def hit_self(self):
        return self.pos in self.body[1:]
