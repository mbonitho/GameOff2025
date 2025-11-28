from enum import Enum
import random
from gameobjects.enemies.enemy_behavior import EnemyBehavior
from utils.parameters import WINDOW_HEIGHT, WINDOW_WIDTH


class SummonMinionBehavior(EnemyBehavior):

    class EnemyType(Enum):
        MOUSE = 0
        CROW = 1


    def __init__(self, enemies, enemyType: EnemyType, obstacles: list = [], objects: list = []):
        super().__init__()
        self.Speed = 100
        self.enemies = enemies
        self.obstacles = obstacles
        self.objects = objects

        self.decision_timing = 0
        self.decision_delay = 3

        self.enemyType = enemyType

    def update(self, enemy, players, dt):
        if len(players) == 0:
            return

        # 
        self.decision_timing += dt   
        if self.decision_timing >= self.decision_delay:
            self.decision_timing %= self.decision_delay
            self.decision_delay = random.randrange(3, 5)

            x = int(random.randrange(enemy.Rect.x - enemy.Surface.get_width(), enemy.Rect.x + enemy.Surface.get_width()))
            if x <= 0 or x >= WINDOW_WIDTH:
                x = enemy.Rect.x

            y = int(random.randrange(enemy.Rect.y - enemy.Surface.get_height(), enemy.Rect.y + enemy.Surface.get_height()))
            if y <= 0 or y >= WINDOW_HEIGHT:
                y = enemy.Rect.y

            match self.enemyType:

                case SummonMinionBehavior.EnemyType.MOUSE:
                    from gameobjects.enemies.enemy_factory import EnemyFactory
                    mouse = EnemyFactory.GetSmallFastEnemy((x, y))
                    self.enemies.append(mouse)

                case SummonMinionBehavior.EnemyType.CROW:
                    from gameobjects.enemies.enemy_factory import EnemyFactory
                    bomber = EnemyFactory.GetBombDropperEnemy((x, y), self.obstacles, self.objects)
                    self.enemies.append(bomber)
