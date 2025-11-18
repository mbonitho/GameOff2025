from gameobjects.enemies.enemy_behavior import EnemyBehavior

class DiesAfterAWhileBehavior(EnemyBehavior):

    def __init__(self, delay: int):
        super().__init__()
        self.lifespan = 0
        self.maxlifespan = delay

    def update(self, enemy, players, dt):
        self.lifespan += dt
        if self.lifespan >= self.maxlifespan:
            enemy.KilledByPlayerIndex = None
            enemy.CurrentLife = 0


    def draw(self, screen, enemy):
        pass