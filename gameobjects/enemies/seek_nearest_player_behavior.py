import math
from gameobjects.enemies.enemy_behavior import EnemyBehavior


class SeekNearestPlayerBehavior(EnemyBehavior):
    def update(self, enemy, players, dt):
        if not players:
            return

        # Find nearest player
        nearest = min(players, key=lambda p: (p.X - enemy.Rect.x)**2 + (p.Y - enemy.Rect.y)**2)
        dx = nearest.X - enemy.Rect.x
        dy = nearest.Y - enemy.Rect.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            enemy.Rect.x += (dx / dist) * enemy.Speed * dt
            enemy.Rect.y += (dy / dist) * enemy.Speed * dt

        enemy.in_attack_range = dist <= enemy.attack_radius