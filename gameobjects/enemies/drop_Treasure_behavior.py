from gameobjects.enemies.enemy_behavior import EnemyBehavior
from utils.helpers.collisions_helper import MoveAndCollide
from gameobjects.objects.objects_factory import ObjectsFactory

class DropTreasureBehavior(EnemyBehavior):

    def __init__(self, objects):
        super().__init__()
        self.Speed = 100
        self.objects = objects



    def update(self, enemy, players, dt):
        if not players:
            return

        if enemy.CurrentLife <= 0: # todo drop treasure instead
            mine = ObjectsFactory.GetLandmine()
            self.objects.append(mine)

