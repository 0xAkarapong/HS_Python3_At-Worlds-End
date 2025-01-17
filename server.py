import socket
import threading
from constant import HOST, PORT

def broadcast(client):
    pass

def handle_client(client):
    pass

#server
def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server started on {HOST}:{PORT}")
        print("Hello")
    
    except socket.error as msg:
        print(f"Socket error: {msg}")
        exit(1)
        
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
