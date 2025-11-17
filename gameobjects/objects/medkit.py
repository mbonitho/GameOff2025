from pygame import  Surface

class Medkit:

    def __init__(self, surface: Surface, x: int, y: int):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)

    def update(self, dt: float):
        pass

    def draw(self, screen):
        screen.blit(self.Surface, self.Rect.topleft)


    def handleCollision(self, player):
        player.CurrentLife = min(player.MaxLife, round(player.CurrentLife * 1.3))

    