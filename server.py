import time
from game.engine import GameState
from game.network import Server
from game.constants import HOST, PORT

def main():
    game_state = GameState()
    server = Server(HOST, PORT)
    server.game_state = game_state
    server.start()
    
    try:
        print(f"Server started on {HOST}:{PORT}")
        
        while True:
            game_state.check_collisions()
            game_state_data = game_state.get_game_state()
            server.broadcast_game_state()
            time.sleep(1 / 60)
            
    except KeyboardInterrupt:
        print("Shutting down server")
    finally:
        server.stop()
        print("Server stopped")

if __name__ == "__main__":
    main()