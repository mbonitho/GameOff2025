from pygame import Surface
from typing import Tuple

class Player:

    def __init__(self, surface: Surface, x: int, y: int, color: Tuple[int, int, int]):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.X = x
        self.Y = y
        self.Tint = color

        self.Speed = 3
        self.MaxLife = 5
        self.Life = self.MaxLife
        self.Score = 0


    def MoveX(self, value):
        self.X += self.Speed * value

    def MoveY(self, value):
        self.Y += self.Speed * value

    def MoveLeft(self, ratio: float = 1):
        self.X -= self.Speed * ratio

    def MoveRight(self, ratio: float = 1):
        self.X += self.Speed * ratio

    def MoveUp(self, ratio: float = 1):
        self.Y -= self.Speed * ratio

    def MoveDown(self, ratio: float = 1):
        self.Y += self.Speed * ratio
