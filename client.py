
import socket
from game.constants import HOST, PORT 

def start_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
        
        while True:
            message = input("Enter message: ")
            client.send(message.encode())
            response = client.recv(1024).decode()
            print(response)
            
    except socket.error as msg:
        print(f"Socket error: {msg}")
        exit(1)
        
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
