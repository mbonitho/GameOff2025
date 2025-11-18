from pygame import  Surface
from gameobjects.blinkingComponent import BlinkingComponent


class Bomb:

    def __init__(self, surfaces: list[Surface], x: int, y: int, objects: list):
        self.Surfaces = surfaces
        self.Rect = surfaces[0].get_rect()
        self.Rect.topleft = (x, y)

        self.objects = objects

        self.lifespan = 0
        self.maxlifespan = 30

        self.BlinkingComponent = BlinkingComponent()

        self.explosionLifespan = 2
        self.ColorBlinkingComponent = BlinkingComponent()
        self.exploded = False

        self.canBePickedUp = False

    def update(self, dt: float):
        self.lifespan += dt
        self.BlinkingComponent.update(dt)
        self.ColorBlinkingComponent.update(dt)

        # blink when about to disappear
        if self.lifespan >= self.explosionLifespan * 0.75 and not self.ColorBlinkingComponent.IsBlinking():
            self.ColorBlinkingComponent.StartBlinking()

        # spawn explosion when at the end of lifespan
        if self.lifespan >= self.explosionLifespan and not self.exploded:
            self.exploded = True
            from gameobjects.objects.objects_factory import ObjectsFactory
            explo = ObjectsFactory.GetExplosion(self.Rect.bottomleft)
            self.objects.append(explo)

    def draw(self, screen):
        if self.ColorBlinkingComponent.visible:
            screen.blit(self.Surfaces[0], self.Rect.topleft)
        else:
            screen.blit(self.Surfaces[1], self.Rect.topleft)

    def handleCollision(self, player):
        pass # no collision while the bomb is armed
