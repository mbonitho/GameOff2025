import math
import random
from gameobjects.enemies.enemy_behavior import EnemyBehavior
from utils.helpers.collisions_helper import MoveAndCollide
from gameobjects.objects.objects_factory import ObjectsFactory
class SpawnMineBehavior(EnemyBehavior):

    def __init__(self, objects):
        super().__init__()
        self.Speed = 100
        self.objects = objects

        self.decision_timing = 0
        self.decision_delay = 1

    def update(self, enemy, players, dt):
        if not players:
            return

        # 
        self.decision_timing += dt   
        if self.decision_timing >= self.decision_delay:
            self.decision_timing %= self.decision_delay
            self.decision_delay = random.randrange(1, 3)

            mine = ObjectsFactory.GetLandmine((enemy.Rect.x, enemy.Rect.y))

            self.objects.append(mine)

