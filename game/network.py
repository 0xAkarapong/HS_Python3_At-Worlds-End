import socket
import threading
import pickle
import time
from game.engine import GameState  # Assuming this is your game logic

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.game_state = GameState()
        self.next_id = 1
        self.running = True  # Flag to control server loop
        self.update_rate = 30  # Update rate in FPS

    def start(self):
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            print(f"Server started on {self.host}:{self.port}")

            accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
            accept_thread.start()

            game_loop_thread = threading.Thread(target=self.game_loop, daemon=True)
            game_loop_thread.start()

            accept_thread.join()
            game_loop_thread.join()
        except OSError as e:
            print(f"Error starting server: {e}")
            self.stop()

    def accept_connections(self):
        while self.running:
            try:
                client, addr = self.server.accept()
                print(f"Connection from {addr}")

                player_id = self.next_id
                self.next_id += 1
                self.clients[player_id] = client
                self.game_state.add_player(player_id)

                client_thread = threading.Thread(target=self.handle_client, args=(client, player_id), daemon=True)
                client_thread.start()

                self.send_to_client(client, {"action": "assign_id", "player_id": player_id})
            except OSError:
                if self.running:
                    print("Error accepting connections.")
                    break

    def handle_client(self, client, player_id):
        while self.running:
            try:
                data = self.receive_from_client(client)
                if not data:
                    break

                action = data.get("action")
                if action == "move":
                    target_x = data.get("target_x")
                    target_y = data.get("target_y")
                    if self.game_state.players.get(player_id): # Check if player exist
                        self.game_state.players[player_id].target_x = target_x
                        self.game_state.players[player_id].target_y = target_y
            except (ConnectionResetError, BrokenPipeError):
                print(f"Client {player_id} disconnected.")
                self.remove_client(player_id)
                break
            except Exception as e:
                print(f"Error handling client {player_id}: {e}")
                self.remove_client(player_id)
                break

    def game_loop(self):
        while self.running:
            start_time = time.time()
            self.broadcast_game_state()
            elapsed_time = time.time() - start_time
            sleep_time = max(1.0 / self.update_rate - elapsed_time, 0)
            time.sleep(sleep_time)

    def send_to_client(self, client, data):
        try:
            client.sendall(pickle.dumps(data))  # Use sendall for complete sends
        except (ConnectionResetError, BrokenPipeError):
            print("Client disconnected during send.")

    def receive_from_client(self, client):
        try:
            data = client.recv(4096)  # Increased buffer size
            if not data:
                return None
            return pickle.loads(data)
        except (EOFError, ConnectionResetError, BrokenPipeError):
            return None

    def broadcast_game_state(self):
        game_state_data = self.game_state.get_game_state()
        for player_id, client in list(self.clients.items()): # Iterate over a copy to avoid issues during removal
            self.send_to_client(client, {"action": "update_game_state", "game_state": game_state_data})

    def remove_client(self, player_id):
        if player_id in self.clients:
            client = self.clients.pop(player_id)
            try:
                client.close()
            except OSError:
                pass
            self.game_state.remove_player(player_id)
            print(f"Removed client {player_id}")

    def stop(self):
        self.running = False
        print("Stopping server...")
        for client in self.clients.values():
            try:
                client.close()
            except OSError:
                pass
        self.server.close()
        print("Server stopped.")

class Client:
    # ... (Client code remains largely the same, with minor improvements below)
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_id = None
        self.running = True

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            threading.Thread(target=self.receive, daemon=True).start()
        except ConnectionRefusedError:
            print("Connection refused. Server might be down.")
            return False
        return True

    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))
        except (ConnectionResetError, BrokenPipeError):
            print("Error sending data. Connection lost.")
            self.disconnect()

    def receive(self):
        while self.running:
            try:
                data = self.client.recv(4096)
                if not data:
                    break
                message = pickle.loads(data)
                self.handle_message(message)
            except (EOFError, ConnectionResetError, BrokenPipeError):
                print("Connection to server lost.")
                self.disconnect()
                break
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.disconnect()
                break

    def handle_message(self, message):
        action = message.get("action")
        if action == "assign_id":
            self.player_id = message["player_id"]
            print(f"Assigned player id: {self.player_id}")
        elif action == "update_game_state":
            game_state = message["game_state"]
            #print(f"Update game state: {game_state}") # Optional print for debug
            pass

    def disconnect(self):
        self.running = False
        try:
            self.client.close()
        except OSError:
            pass
        print("Disconnected from server.")