from pygame import Surface

from gameobjects.enemies.enemy_behavior import EnemyBehavior

class Enemy:
    def __init__(self, surface: Surface, x: int, y: int, behaviors: list[EnemyBehavior]):      
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)
        self.Behaviors = behaviors

        self.MaxHP = 5

    def update(self, players, dt: float):
        for beh in self.Behaviors:
            beh.update(self, players, dt)

    def draw(self, screen):
        screen.blit(self.Surface, self.Rect.topleft)

        for beh in self.Behaviors:
            beh.draw(screen, self)

    def ReceiveDamage(self):
        pass