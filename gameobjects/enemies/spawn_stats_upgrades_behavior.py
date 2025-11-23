from gameobjects.enemies.enemy_behavior import EnemyBehavior

from gameobjects.objects.objects_factory import ObjectsFactory
from utils.parameters import WINDOW_HEIGHT, WINDOW_WIDTH

class SpawnStatsUpgradesBehavior(EnemyBehavior):

    def __init__(self, upgradeValue: int, objects: list):
        super().__init__()
        self.Speed = 100
        self.objects = objects
        self.upgradeValue = upgradeValue



    def update(self, enemy, players, dt):
        if len(players) == 0:
            return

        if enemy.CurrentLife <= 0:

            if players[0].CurrentLife > 0:
                pickup = ObjectsFactory.GetMaxLifeUp((WINDOW_WIDTH * 0.25, WINDOW_HEIGHT * .25), self.upgradeValue)
                self.objects.append(pickup)

                pickup = ObjectsFactory.GetMaxLifeUp((WINDOW_WIDTH * 0.75, WINDOW_HEIGHT * .25), self.upgradeValue)
                self.objects.append(pickup)

            # if len(players) > 1 and players[1].CurrentLife > 0: