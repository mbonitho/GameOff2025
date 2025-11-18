from pygame import  Surface
from gameobjects.blinkingComponent import BlinkingComponent

class Explosion:

    def __init__(self, surface: Surface, x: int, y: int):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)

        self.lifespan = 0
        self.maxlifespan = 1

        self.canBePickedUp = False

        # unused for Explosions
        self.BlinkingComponent = BlinkingComponent()

    def update(self, dt: float):
        self.lifespan += dt

    def draw(self, screen):
        screen.blit(self.Surface, self.Rect.topleft)

    def handleCollision(self, player):
        if self.lifespan < self.maxlifespan:
            if player.ReceiveDamage(2):
                player.BlinkingComponent.StartBlinking()
