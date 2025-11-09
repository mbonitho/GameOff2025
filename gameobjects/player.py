from pygame import Rect, Surface
from typing import Tuple
from gameobjects.blinkingComponent import BlinkingComponent
from utils.helpers.collisions_helper import MoveAndCollide

class Player:

    def __init__(self, surface: Surface, x: int, y: int, color: Tuple[int, int, int]):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)
        self.Tint = color

        self.Speed = 6
        self.MaxLife = 5
        self.CurrentLife = self.MaxLife
        self.Score = 0

        self.MaxBullets = 3
        self.Bullets = []

        self.BlinkingComponent = BlinkingComponent()


    def update(self, dt: float):
        self.BlinkingComponent.update(dt)


    def draw(self, screen):
        if self.BlinkingComponent.visible:
            screen.blit(self.Surface, self.Rect.topleft)

    def MoveX(self, value, obstacles: list[Rect]):
        #self.Rect.x += self.Speed * value
        MoveAndCollide(self.Rect, self.Speed * value, 0, obstacles)

    def MoveY(self, value, obstacles: list[Rect]):
        #self.Rect.y += self.Speed * value
        MoveAndCollide(self.Rect, 0, self.Speed * value, obstacles)

    def MoveLeft(self, obstacles: list[Rect], ratio: float = 1):
        #self.Rect.x -= int(self.Speed * ratio)
        MoveAndCollide(self.Rect, int(self.Speed * ratio) * -1, 0, obstacles)


    def MoveRight(self, obstacles: list[Rect], ratio: float = 1):
        #self.Rect.x += int(self.Speed * ratio)
        MoveAndCollide(self.Rect, int(self.Speed * ratio), 0, obstacles)

    def MoveUp(self, obstacles: list[Rect], ratio: float = 1):
        #self.Rect.y -= int(self.Speed * ratio)
        MoveAndCollide(self.Rect, 0, int(self.Speed * ratio) * -1, obstacles)

    def MoveDown(self, obstacles: list[Rect], ratio: float = 1):
        #self.Rect.y += int(self.Speed * ratio)
        MoveAndCollide(self.Rect, 0, int(self.Speed * ratio), obstacles)

    def ReceiveDamage(self):
        # invicibility fames
        if not self.BlinkingComponent.IsBlinking():
            self.BlinkingComponent.StartBlinking()
            self.CurrentLife -= 1

    def TryShootBullet(self, bullet):

        if len(self.Bullets) < self.MaxBullets:
            self.Bullets.append(bullet)