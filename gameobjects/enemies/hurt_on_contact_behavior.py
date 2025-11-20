from gameobjects.enemies.enemy_behavior import EnemyBehavior

class HurtOnContactBehavior(EnemyBehavior):

    def __init__(self, dmg: int = 1):
        super().__init__()
        self.damage = dmg

    def update(self, enemy, players, dt):
        # hurt players in contact
        for player in players:
            if enemy.Rect.colliderect(player.Rect):
                player.ReceiveDamage(self.damage)


    def draw(self, screen, enemy):
        pass