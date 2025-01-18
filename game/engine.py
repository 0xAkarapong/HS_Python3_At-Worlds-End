# Engine part
from utils import *
from game.constants import *
import random
class Player:
    def __init__(self, player_id, x, y, color,radius=STARTING_RADIUS):
        self.player_id = player_id
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
    
    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "radius": self.radius
        }

class Food:
    def __init__(self, x, y, color, radius=FOOD_RADIUS):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "radius": self.radius
        }
    
class GameState:
    def __init__(self):
        self.players = {}
        self.foods = []
        self.generate_food(INITIAL_FOODS_COUNT)


    def add_player(self, player_id):
        x,y = self.get_random_position()
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.players[player_id] = Player(player_id, x, y, color)

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
