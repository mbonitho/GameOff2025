from gameobjects.enemies.enemy_behavior import EnemyBehavior

class HurtOnContactBehavior(EnemyBehavior):

    def __init__(self):
        super().__init__()

    def update(self, enemy, players, dt):
        # hurt players in contact
        for player in players:
            if enemy.Rect.colliderect(player.Rect):
                player.ReceiveDamage()


    def draw(self, screen, enemy):
        pass