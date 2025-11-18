from enum import Enum
import random
from gameobjects.enemies.enemy_behavior import EnemyBehavior


class SummonMinionBehavior(EnemyBehavior):

    class EnemyType(Enum):
        MOUSE = 0


    def __init__(self, enemies, enemyType: EnemyType):
        super().__init__()
        self.Speed = 100
        self.enemies = enemies

        self.decision_timing = 0
        self.decision_delay = 3

        self.enemyType = enemyType

    def update(self, enemy, players, dt):
        if not players:
            return

        # 
        self.decision_timing += dt   
        if self.decision_timing >= self.decision_delay:
            self.decision_timing %= self.decision_delay
            self.decision_delay = random.randrange(3, 5)

            match self.enemyType:

                case SummonMinionBehavior.EnemyType.MOUSE:
                    from gameobjects.enemies.enemy_factory import EnemyFactory
                    mouse = EnemyFactory.GetSmallFastEnemy((enemy.Rect.x, enemy.Rect.y))
                    self.enemies.append(mouse)

