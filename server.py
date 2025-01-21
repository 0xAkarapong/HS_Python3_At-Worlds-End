import time
from game.network import Server, logging, RotatingFileHandler
from game.engine import GameState  # Import GameState
from game.constants import *

logger = logging.getLogger("ServerLogger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("server.log", maxBytes=10000000, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    game_state = GameState()  # Create game_state first
    server = Server(HOST, PORT, game_state)  # Pass game_state to Server

    try:
        server.start()
        logger.info(f"Server started on {HOST}:{PORT}")

        # Main game loop (on a separate thread or process for production)
        while True:
            server.update_clients()
            game_state.update()
            time.sleep(1 / SERVER_TICK_RATE)  # Control server tick rate

    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    finally:
        server.stop()


if __name__ == "__main__":
    main()