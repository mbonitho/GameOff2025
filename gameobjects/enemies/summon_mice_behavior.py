import random
from gameobjects.enemies.enemy_behavior import EnemyBehavior


class SummonMiceBehavior(EnemyBehavior):

    def __init__(self, enemies):
        super().__init__()
        self.Speed = 100
        self.enemies = enemies

        self.decision_timing = 0
        self.decision_delay = 3

    def update(self, enemy, players, dt):
        if not players:
            return

        # 
        self.decision_timing += dt   
        if self.decision_timing >= self.decision_delay:
            self.decision_timing %= self.decision_delay
            self.decision_delay = random.randrange(3, 5)

            from gameobjects.enemies.enemy_factory import EnemyFactory
            mouse = EnemyFactory.GetSmallFastEnemy((enemy.Rect.x, enemy.Rect.y))

            self.enemies.append(mouse)

