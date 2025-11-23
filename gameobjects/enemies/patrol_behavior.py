from pygame import Rect
from gameobjects.enemies.enemy_behavior import EnemyBehavior
from utils.helpers.collisions_helper import MoveAndCollide

class PatrolBehavior(EnemyBehavior):

    def __init__(self, obstacles: list[Rect], direction: str):
        super().__init__()
        self.Speed = 80
        self.obstacles = obstacles


        self.direction = direction
        self.factor = 1

    def update(self, enemy, players, dt):
        if len(players) == 0:
            return

        x_dest = 0 
        y_dest = 0 
        
        if self.direction == 'h':
            x_dest += self.Speed * dt * self.factor
    
        elif self.direction == 'v':
            y_dest += self.Speed * dt * self.factor

        collisions = MoveAndCollide(enemy.Rect, x_dest, y_dest, self.obstacles)

        if collisions != (0,0):
            self.factor *= -1

