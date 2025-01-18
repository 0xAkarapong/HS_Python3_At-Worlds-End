import math

def circle_collion(obj1, obj2) -> bool:
    """Checks for collision between two circle objects (e.g., Player, Food)."""
    distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
    return distance < obj1.radius + obj2.radius