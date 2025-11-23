import random
from gameobjects.enemies.enemy_behavior import EnemyBehavior
from utils.helpers.collisions_helper import MoveAndCollide
from gameobjects.objects.objects_factory import ObjectsFactory

class DropTreasureBehavior(EnemyBehavior):

    def __init__(self, objects):
        super().__init__()
        self.Speed = 100
        self.objects = objects



    def update(self, enemy, players, dt):
        if len(players) == 0:
            return

        if enemy.CurrentLife <= 0:
            bag = ObjectsFactory.GetMoneyBag(enemy.Rect.topleft, random.randrange(100, 500, step=50))
            self.objects.append(bag)

