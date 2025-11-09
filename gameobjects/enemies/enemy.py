from pygame import Surface
from gameobjects.blinkingComponent import BlinkingComponent
from gameobjects.enemies.enemy_behavior import EnemyBehavior

class Enemy:
    def __init__(self, surface: Surface, x: int, y: int, behaviors: list[EnemyBehavior]):      
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)
        self.Behaviors = behaviors

        self.BlinkingComponent = BlinkingComponent()
        self.BlinkingComponent.total_blinking_duration = 0.3 # seconds

        self.MaxLife = 2
        self.CurrentLife =  self.MaxLife

    def update(self, players, dt: float):
        self.BlinkingComponent.update(dt)
        for beh in self.Behaviors:
            beh.update(self, players, dt)

    def draw(self, screen):
        if self.BlinkingComponent.visible:
            screen.blit(self.Surface, self.Rect.topleft)

            for beh in self.Behaviors:
                beh.draw(screen, self)

    def ReceiveDamage(self):
        if not self.BlinkingComponent.IsBlinking():
            self.BlinkingComponent.StartBlinking()
            self.CurrentLife -= 1
