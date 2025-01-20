import pygame
from game.constants import *

class GameWindow:
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.screen = pygame.display.set_mode((width, height))  # Set window size
        self.screen.fill(BG_COLOR)  # Fill background initially

    def render_game_objects(self, game_state_dict, local_player_id):
        # Render food
        for food_data in game_state_dict["food"]:
            pygame.draw.circle(self.screen, food_data["color"], (food_data["x"], food_data["y"]), food_data["radius"])

        # Render players
        for player_id, player_data in game_state_dict["players"].items():
            # Draw a thicker circle for the local player
            line_width = 3 if player_id == local_player_id else 0
            pygame.draw.circle(self.screen, player_data["color"], (player_data["x"], player_data["y"]),
                               player_data["radius"], line_width)