import pygame
import random
from game.utils import circle_collision, point_in_circle
from game.constants import *


class Player:
    def __init__(self, player_id, x, y, color, radius=STARTING_RADIUS):
        self.id = player_id
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.target_x = x  # For mouse-based movement
        self.target_y = y

    def move(self):
        # Basic movement towards the target (mouse position)
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist > 0:
            # Normalize
            dx = dx / dist
            dy = dy / dist

        # Limit speed based on radius
        speed = MAX_SPEED / (self.radius ** 0.5)

        self.x += dx * speed
        self.y += dy * speed

        # Keep within bounds (simple for now, improve in utils.py)
        self.x = max(0, min(self.x, GAME_WIDTH))
        self.y = max(0, min(self.y, GAME_HEIGHT))

    def eat(self, food):
        # Increase size based on the food's radius (or a fixed amount)
        self.radius += food.radius * 0.2  # Adjust growth rate as needed

    def to_dict(self):
        return {
            "id": self.id,
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
        self.eaten = False  # Flag for removal

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "radius": self.radius
        }


class GameState:
    def __init__(self):
        self.players = {}
        self.food = []
        self.generate_food(INITIAL_FOOD_COUNT)

    def add_player(self, player_id):
        x, y = self.get_random_position()
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.players[player_id] = Player(player_id, x, y, color)

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    def update_player_input(self, player_id, data):
        if player_id in self.players:
            player = self.players[player_id]
            player.target_x = data["x"]
            player.target_y = data["y"]

    def generate_food(self, count):
        for _ in range(count):
            x, y = self.get_random_position()
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.food.append(Food(x, y, color))

    def get_random_position(self):
        # Improve this function for production to avoid overlaps
        x = random.randint(0, GAME_WIDTH)
        y = random.randint(0, GAME_HEIGHT)
        return x, y

    def update(self):
        # Player movement
        for player in self.players.values():
            player.move()

        # Collision detection and eating
        for player in self.players.values():
            for i in reversed(range(len(self.food))):  # Iterate in reverse for safe removal
                food = self.food[i]
                if point_in_circle(food.x, food.y, player.x, player.y, player.radius):
                    player.eat(food)
                    food.eaten = True  # Mark as eaten

            # Player-player collisions
            for other_player in self.players.values():
                if player.id != other_player.id:
                    if circle_collision(player, other_player):
                        if player.radius > other_player.radius * 1.10:  # 10% bigger
                            player.eat(other_player)
                            self.remove_player(other_player.id)
                        elif other_player.radius > player.radius * 1.10:
                            other_player.eat(player)
                            self.remove_player(player.id)

        # Remove eaten food
        self.food = [f for f in self.food if not f.eaten]

        # Replenish food (basic, improve in production)
        if len(self.food) < MAX_FOOD:
            self.generate_food(FOOD_GENERATION_RATE)

    def get_game_state(self):
        # Convert game state to a dictionary for JSON serialization
        return {
            "players": {player_id: player.to_dict() for player_id, player in self.players.items()},
            "food": [food.to_dict() for food in self.food]
        }