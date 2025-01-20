import math

def circle_collision(obj1, obj2):
    """Checks for collision between two circle objects (e.g., Player, Food)."""
    distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
    return distance < (obj1.radius + obj2.radius)

def point_in_circle(px, py, cx, cy, radius):
    """Checks if a point (px, py) is within a circle."""
    distance = math.sqrt((px - cx)**2 + (py - cy)**2)
    return distance < radius