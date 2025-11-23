import math
from gameobjects.enemies.enemy_behavior import EnemyBehavior


class SeekNearestPlayerBehavior(EnemyBehavior):

    def __init__(self):
        super().__init__()
        self.Speed = 100

    def update(self, enemy, players, dt):
        if len(players) == 0:
            return

        # Find nearest player
        nearest = min(players, key=lambda p: (p.Rect.x - enemy.Rect.x)**2 + (p.Rect.y - enemy.Rect.y)**2)
        dx = nearest.Rect.x - enemy.Rect.x
        dy = nearest.Rect.y - enemy.Rect.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            enemy.Rect.x += (dx / dist) * self.Speed * dt
            enemy.Rect.y += (dy / dist) * self.Speed * dt
