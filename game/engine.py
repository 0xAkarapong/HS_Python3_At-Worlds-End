# Engine part
from utils import *
from game.constants import *
class Player:
    def __init__(self, x, y, color,radius=STARTING_RADIUS):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.target_x = x
        self.target_y = y
    def move(self):
        # Basic movement towards the target (mouse position)
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx = dx / distance
            dy = dy / distance

        speed = MAX_SPEED / math.sqrt(self.radius)

        self.x += dx * speed
        self.y += dy * speed

        self.x = max(0, min(self.x, GAME_WIDTH))
        self.y = max(0, min(self.y, GAME_HEIGHT))

    def eat(self, food):
        self.radius += food.radius * 0.2

class Food:
    def __init__(self):
        pass

