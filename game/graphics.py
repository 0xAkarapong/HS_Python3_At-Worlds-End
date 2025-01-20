import pygame
import os

class GameWindow:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("At World's End")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load assets
        self.sprite_manager = SpriteManager()
        self.camera = Camera(width, height)
        
        # Background
        self.background = self.sprite_manager.load_background("background.png")

    def render(self, game_state):
        self.screen.fill((0, 0, 0))  # Clear screen
        
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw all players
        for player_id, player in game_state['players'].items():
            pos = self.camera.world_to_screen(player)
            pygame.draw.circle(self.screen, player['color'], (int(pos[0]), int(pos[1])), int(player['radius']))
        
        # Draw all foods
        for food in game_state['foods']:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(food['x']), int(food['y'])), int(food['radius']))
        
        pygame.display.flip()
        self.clock.tick(60)

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
    
    def follow(self, target):
        self.x = target['x'] - self.width // 2
        self.y = target['y'] - self.height // 2
    
    def world_to_screen(self, entity):
        return (entity['x'] - self.x, entity['y'] - self.y)

class SpriteManager:
    def __init__(self):
        self.sprite_cache = {}
        self.asset_path = os.path.join(os.path.dirname(__file__), '../assets')
    
    def load_sprite(self, filename):
        if filename not in self.sprite_cache:
            path = os.path.join(self.asset_path, filename)
            self.sprite_cache[filename] = pygame.image.load(path).convert_alpha()
        return self.sprite_cache[filename]
    
    def load_background(self, filename):
        path = os.path.join(self.asset_path, filename)
        return pygame.image.load(path).convert()