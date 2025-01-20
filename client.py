import pygame
from game.network import Client
from game.constants import HOST, PORT

if __name__ == "__main__":
    client = Client(HOST, PORT)
    client.connect()

    while client.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.running = False
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                client.send({"action": "move", "x": x, "y": y})
        pygame.time.wait(100)