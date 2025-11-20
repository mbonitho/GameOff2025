from pygame import  Surface
from gameobjects.blinkingComponent import BlinkingComponent


class HelpButton:

    def __init__(self, surface: Surface, x: int, y: int, textkey):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)

        self.textKey = textkey

    def update(self, dt: float):
        pass

    def draw(self, screen):
        screen.blit(self.Surface, self.Rect.topleft)

    def handleCollision(self, player):
        pass
