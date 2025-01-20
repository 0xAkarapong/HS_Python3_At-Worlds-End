# Engine part
from game.utils import *
from game.constants import *
import random

class Food:
    def __init__(self, x: int, y: int, color: tuple, radius: float=FOOD_RADIUS):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.eaten = False

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "radius": self.radius,
            "eaten": self.eaten
        }

class Player:
    def __init__(self, player_id: int, x: int, y:int , color: tuple, radius: float=STARTING_RADIUS):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.target_x = x
        self.target_y = y
    
    def move(self) -> None:
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

    def eat(self, food: Food) -> None:
        self.radius += food.radius * 0.2
    
    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
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


    def add_player(self, player_id: int) -> None:
        x,y = self.get_random_position()
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.players[player_id] = Player(player_id, x, y, color)

    def remove_player(self, player_id: int) -> None:
        if player_id in self.players:
            del self.players[player_id]

    def generate_food(self, count: int) -> None:
        for _ in range(count):
            x,y = self.get_random_position()
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.foods.append(Food(x, y, color))
    
    def get_random_position(self) -> tuple:
        x = random.randint(0, GAME_WIDTH)
        y = random.randint(0, GAME_HEIGHT)
        return x, y

    def update(self) -> None:
        # Player Movement
        for player in self.players.values():
            player.move()
        
        # Collision Detection and eating food
        for player in self.players.values():
            for i in reversed(range(len(self.foods))):
                food = self.foods[i]
                if circle_collion(player, food):
                    player.eat(food)
                    del self.foods[i]
        
        # Player Collision
        for other_player in self.players.values():
            for player in self.players.values():
                if player.player_id == other_player.player_id:
                    continue
                if circle_collion(player, other_player):
                    if player.radius > other_player.radius:
                        player.radius += other_player.radius * 0.2
                        del self.players[other_player.player_id]
                    elif player.radius < other_player.radius:
                        other_player.radius += player.radius * 0.2
                        del self.players[player.player_id]
                        
        # Remove eaten food
        self.foods = [food for food in self.foods if not food.eaten]
    def get_game_state(self) -> dict:
        players = [player.to_dict() for player in self.players.values()]
        foods = [food.to_dict() for food in self.foods]
        return {
            "players": players,
            "foods": foods
        }
