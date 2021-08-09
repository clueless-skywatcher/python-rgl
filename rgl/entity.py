import tcod

class Entity:
    def __init__(self, x, y, char, color) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        self.x += dx
        self.y += dy