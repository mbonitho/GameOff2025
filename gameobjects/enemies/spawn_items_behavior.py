import random
from gameobjects.enemies.enemy_behavior import EnemyBehavior
from enum import Enum

from utils.parameters import WINDOW_HEIGHT, WINDOW_WIDTH

class SpawnItemBehavior(EnemyBehavior):

    class ObjectType(Enum):
        MINE = 0
        BOMB = 1
        MONEY = 2


    def __init__(self, objects, objectType: ObjectType):
        super().__init__()
        self.Speed = 100
        self.objects = objects

        self.decision_timing = 0
        self.decision_delay = 1

        self.decisionMinTime: float = 1
        self.decisionMaxTime: float = 3

        self.objectType = objectType

    def update(self, enemy, players, dt):
        if len(players) == 0:
            return

        # 
        self.decision_timing += dt   
        if self.decision_timing >= self.decision_delay:
            self.decision_timing %= self.decision_delay
            self.decision_delay = self.decisionMinTime + random.random() * (self.decisionMaxTime - self.decisionMinTime)

            x = int(random.randrange(enemy.Rect.x - enemy.Surface.get_width(), enemy.Rect.x + enemy.Surface.get_width()))
            if x <= 0 or x >= WINDOW_WIDTH:
                x = enemy.Rect.x

            y = int(random.randrange(enemy.Rect.y - enemy.Surface.get_height(), enemy.Rect.y + enemy.Surface.get_height()))
            if y <= 0 or y >= WINDOW_HEIGHT:
                y = enemy.Rect.y

            match self.objectType:

                case SpawnItemBehavior.ObjectType.MINE:
                    from gameobjects.objects.objects_factory import ObjectsFactory
                    item = ObjectsFactory.GetLandmine((x, y))
                    self.objects.append(item)

                case SpawnItemBehavior.ObjectType.BOMB:
                    from gameobjects.objects.objects_factory import ObjectsFactory
                    item = ObjectsFactory.GetBomb((x, y), self.objects)
                    self.objects.append(item)

                case SpawnItemBehavior.ObjectType.MONEY:
                    from gameobjects.objects.objects_factory import ObjectsFactory
                    item = ObjectsFactory.GetMoneyBag((x, y), random.randrange(5, 31, 5))
                    self.objects.append(item)        
