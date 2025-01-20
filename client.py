import pygame
import json
from game.network import Client
from game.engine import Player, Food
from game.graphics import GameWindow
from game.constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Agar.io")
    clock = pygame.time.Clock()

    client = Client(HOST, PORT)

    try:
        client.connect()
        player_id = client.receive()  # Initial message will be the player ID
        print(f"Connected as Player {player_id}")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Get player input
            mouse_x, mouse_y = pygame.mouse.get_pos()
            client.send({"type": "input", "x": mouse_x, "y": mouse_y})

            # Receive and process game state
            data = client.receive()
            if data:
                game_state_dict = json.loads(data)

                # Clear the screen
                screen.fill(BG_COLOR)

                # Update and render game objects (players, food)
                GameWindow.render_game_objects(screen, game_state_dict, player_id)

                pygame.display.flip()
            clock.tick(CLIENT_FPS)

    except ConnectionRefusedError:
        print("Failed to connect to the server.")
    finally:
        client.disconnect()
        pygame.quit()

if __name__ == "__main__":
    main()