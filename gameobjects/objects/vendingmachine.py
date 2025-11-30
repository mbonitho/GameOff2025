from pygame import  Surface
from gameobjects.blinkingComponent import BlinkingComponent
from utils.sfx_factory import SFXFactory

class VendingMachine:

    def __init__(self, surface: Surface, x: int, y: int):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)

        self.CollissionRect =  self.Rect.inflate(20, 20)

        self.lifespan = 0
        self.maxlifespan = 20

        self.BlinkingComponent = BlinkingComponent()

        self.canBePickedUp = False

    def update(self, dt: float):
        pass

    def draw(self, screen):
        screen.blit(self.Surface, self.Rect.topleft)

    def handleCollision(self, player):
        if player.Rect.colliderect(self.CollissionRect) and player.CurrentLife < player.MaxLife:
            player.CurrentLife = player.MaxLife
            SFXFactory.PlayPlayerDrinksSFX(player.playerIndex) 
    