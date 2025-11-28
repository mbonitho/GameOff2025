import math
import random
from gameobjects.enemies.enemy_behavior import EnemyBehavior
from utils.helpers.collisions_helper import MoveAndCollide
from utils.parameters import WINDOW_HEIGHT, WINDOW_WIDTH

class MoveRandomlyBehavior(EnemyBehavior):

    def __init__(self, obstacles, decisionDelay: int = 1):
        super().__init__()
        self.Speed = 100
        self.obstacles = obstacles

        self.decision_timing = 0
        self.decision_delay = decisionDelay
        self.destination_x = random.randrange(200, 800)
        self.destination_y = random.randrange(200, 600)

    def update(self, enemy, players, dt):
        if len(players) == 0:
            return

        # 
        self.decision_timing += dt

        destinationReached = abs(enemy.Rect.x - self.destination_x) < 5 and abs(enemy.Rect.y - self.destination_y) < 5
        if self.decision_timing >= self.decision_delay or destinationReached:
            self.decideNewDestination()

        dx = self.destination_x - enemy.Rect.x
        dy = self.destination_y - enemy.Rect.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            x_dest = (dx / dist) * self.Speed * dt
            y_dest = (dy / dist) * self.Speed * dt
            collisions = MoveAndCollide(enemy.Rect, x_dest, y_dest, self.obstacles)
            if collisions != (0,0):
                 self.decideNewDestination()

    def decideNewDestination(self):
            self.decision_timing %= self.decision_delay
            # self.decision_delay = 5
            self.destination_x = random.randrange(96, WINDOW_WIDTH - 96)
            self.destination_y = random.randrange(96, WINDOW_HEIGHT - 96)
