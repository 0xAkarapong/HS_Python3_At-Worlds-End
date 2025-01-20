import time
from game.network import Server
from game.engine import GameState  # Import GameState
from game.constants import *


def main():
    game_state = GameState()  # Create game_state first
    server = Server(HOST, PORT, game_state)  # Pass game_state to Server

    try:
        server.start()
        print(f"Server started on {HOST}:{PORT}")

        # Main game loop (on a separate thread or process for production)
        while True:
            server.update_clients()
            game_state.update()
            time.sleep(1 / SERVER_TICK_RATE)  # Control server tick rate

    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server.stop()


if __name__ == "__main__":
    main()