from pygame import  Surface
from gameobjects.blinkingComponent import BlinkingComponent
from utils.sfx_factory import SFXFactory

class Medkit:

    def __init__(self, surface: Surface, x: int, y: int):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)

        self.lifespan = 0
        self.maxlifespan = 20

        self.BlinkingComponent = BlinkingComponent()

        self.canBePickedUp = True

    def update(self, dt: float):
        self.lifespan += dt
        self.BlinkingComponent.update(dt)

        # blink when about to disappear
        if self.lifespan >= self.maxlifespan * 0.75 and not self.BlinkingComponent.IsBlinking():
            self.BlinkingComponent.StartBlinking()

    def draw(self, screen):
        screen.blit(self.Surface, self.Rect.topleft)

    def handleCollision(self, player):
        if self.lifespan < self.maxlifespan:
            player.CurrentLife = min(player.MaxLife, max(player.CurrentLife + 1, round(player.CurrentLife * 1.3)))
            SFXFactory.PlayPlayerHealedSFX(player.playerIndex) 


    