import socket
import threading
import pickle
from  game.engine import GameState

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {} 
        self.game_state = GameState()
        self.next_id = 1
        
    #start server
    def start(self):
        self.server.bind(self.host, self.port)
        self.server.listen()
        threading.Thread(target=self.accept_connects, daemon=True).start()
        print(f"Server started on {self.host}:{self.port}")

       
    
    def accept_connects(self):
        while True:
            client, addr = self.server.accept()
            print(f"Connection from {addr}")
                
            player_id = self.next_id
            self.next_id += 1              
            self.clients[player_id] = client
            self.game_state.add_player(player_id) # add player
            
            threading.Thread(target=self.handle_client, args=(client, player_id), daemon=True).start()
                
             # send player id to client
            self.send_to_client(client, {"action": "assign", "player_id": player_id})
    
    
    def handle_client(self, client, player_id):
        while True:
            try:
                data = self.receive_from_client(client)
                if not data:
                    break
                
                action = data.get("action")
                if action == "move":
                    #uppdate player position
                    target_x = data.get["target_x"]
                    target_y = data.get["target_y"]
                    self.game_state.players[player_id].target_x = target_x
                    self.game_state.players[player_id].target_y = target_y
                    
                    #send to players
            except Exception as e:
                print(f"Error handling client {player_id}: {e}")
                break
     
    
    def send_to_client(self, client, data):
        try:
            client.send(pickle.dumps(data))
        except Exception as e:
            print(f"Error sending data to client: {e}")
        
    
    def receive_frome_client(self, client):
        try:
            data = client.recv(32)
            return pickle.loads(data) #Deserialize data
        except Exception as e:
            print(f"Error receiving data from client: {e}")
            return None
    
    
    def broadcast_game_state(self):
        #send game state to all clients
        game_state_data = self.game_state.get_game_state()
        for client in self.clients.values():
            self.send_to_client(client, {"acion": "update_game_state", "game_state": game_state_data})
    
    def stop(self):
        print("Stopping server...")
        for client in self.clients.values():
            try:
                client.close()
            except:
                pass
        self.server.close()
        print("Server stopped.")

        
    
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_id = None
    
    def connect(self):
        self.client.connect((self.host, self.port))
        threading.Thread(target=self.receive, daemon=True).start()
        
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except Exception as e:
            print(f"Error sending data: {e}")
    
    def receive(self):
        while True:
            try:
                data = self.client.recv(32)
                if not data:
                    break
                message = pickle.loads(data)
                self.handle_message(message)
            except Exception as e:
                print(f"Error recieving data: {e}")
                break
            
    def handle_message(self, message):
        action = message.get("action")
        if action == "assign_id":
            self.player_id = message["player_id"]
            print(f"Assigned player id: {self.player_id}")
        elif action == "update_game_state":
            game_state = message["game_state"]
            print(f"Update game state: {game_state}")
            
    
    def disconnect(self):
        self.client.close()
    
   
    
      