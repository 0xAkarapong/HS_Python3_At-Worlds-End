import socket
import threading
import json
import struct
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("ServerLogger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("server.log", maxBytes=10000000, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Server:
    def __init__(self, host, port, game_state):  # Add game_state as parameter
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}  # Keep track of connected clients and their associated player IDs
        self.next_player_id = 1
        self.game_state = game_state  # Store game_state as an instance variable

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            logger.info(f"Connection from {client_address} established!")

            player_id = self.next_player_id
            self.next_player_id += 1

            self.clients[player_id] = client_socket
            threading.Thread(target=self.handle_client, args=(client_socket, player_id), daemon=True).start()

            # Send the player their ID
            self.send_to_client(client_socket, player_id)

    def handle_client(self, client_socket, player_id):
        # Add player to the game
        self.game_state.add_player(player_id)  # Use self.game_state

        while True:
            try:
                data = self.receive_from_client(client_socket)
                if not data:
                    break

                # Process client input
                if data["type"] == "input":
                    self.game_state.update_player_input(player_id, data)

                # Add other command processing logic here

            except (ConnectionResetError, BrokenPipeError):
                logger.info(f"Client {player_id} disconnected.")
                break

        # Remove player from the game and close the connection
        self.game_state.remove_player(player_id)
        del self.clients[player_id]
        client_socket.close()

    def send_to_client(self, client_socket, data):
        try:
            serialized_data = json.dumps(data).encode('utf-8')
            # Prefix the message with its length
            message = struct.pack('>I', len(serialized_data)) + serialized_data
            client_socket.sendall(message)
            logger.info(f"Sent to client: {data['players']}")
        except (ConnectionResetError, BrokenPipeError) as e:
            logger.info(f"Error sending to client: {e}")

    def receive_from_client(self, client_socket):
        try:
            # Receive the message length
            raw_message_length = self.recvall(client_socket, 4)
            if not raw_message_length:
                return None
            message_length = struct.unpack('>I', raw_message_length)[0]
            # Receive the actual data
            data = self.recvall(client_socket, message_length)
            if data:
                logger.info(f"Received from client: {data}")
                return json.loads(data.decode('utf-8'))
            else:
                return None
        except json.JSONDecodeError:
            logging.info("Invalid JSON received from client.")
            return None
        except (ConnectionResetError, BrokenPipeError) as e:
            return None

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def update_clients(self):
        game_state_dict = self.game_state.get_game_state()  # Use self.game_state
        for client_socket in self.clients.values():
            self.send_to_client(client_socket, game_state_dict)

    def stop(self):
        for client_socket in self.clients.values():
            client_socket.close()
        self.server_socket.close()


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))

    def send(self, data):
        serialized_data = json.dumps(data).encode('utf-8')
        # Prefix the message with its length
        message = struct.pack('>I', len(serialized_data)) + serialized_data
        self.client_socket.sendall(message)

    def receive(self):
        try:
            # Receive the message length
            raw_message_length = self.recvall(4)
            if not raw_message_length:
                return None
            message_length = struct.unpack('>I', raw_message_length)[0]
            # Receive the actual data
            data = self.recvall(message_length)
            if data:
                return data.decode('utf-8')
            else:
                return None
        except json.JSONDecodeError:
            print("Invalid JSON received from server")
            return None

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = self.client_socket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def disconnect(self):
        self.client_socket.close()