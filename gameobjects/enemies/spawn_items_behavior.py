import random
from gameobjects.enemies.enemy_behavior import EnemyBehavior
from enum import Enum

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

        self.decisionMinTime = 1
        self.decisionMaxTime = 3

        self.objectType = objectType

    def update(self, enemy, players, dt):
        if not players:
            return

        # 
        self.decision_timing += dt   
        if self.decision_timing >= self.decision_delay:
            self.decision_timing %= self.decision_delay
            self.decision_delay = self.decisionMinTime + random.random() * (self.decisionMaxTime - self.decisionMinTime)

            match self.objectType:

                case SpawnItemBehavior.ObjectType.MINE:
                    from gameobjects.objects.objects_factory import ObjectsFactory
                    item = ObjectsFactory.GetLandmine((enemy.Rect.x, enemy.Rect.y))
                    self.objects.append(item)

                case SpawnItemBehavior.ObjectType.BOMB:
                    from gameobjects.objects.objects_factory import ObjectsFactory
                    item = ObjectsFactory.GetBomb((enemy.Rect.x, enemy.Rect.y), self.objects)
                    self.objects.append(item)

                case SpawnItemBehavior.ObjectType.MONEY:
                    from gameobjects.objects.objects_factory import ObjectsFactory
                    item = ObjectsFactory.GetMoneyBag((enemy.Rect.x, enemy.Rect.y), random.randrange(5, 31, 5))
                    self.objects.append(item)        
