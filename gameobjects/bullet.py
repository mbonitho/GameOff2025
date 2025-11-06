from pygame import Surface
from typing import Tuple

class Bullet:

    def __init__(self, surface: Surface, x: int, y: int, x_dir: int, y_dir: int):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.X = x
        self.Y = y
        self.X_dir = x_dir
        self.Y_dir = y_dir
        
        self.Speed = 5 # default speed

        self.lifespan = 0
        self.max_lifespan = 3

    def update(self, dt: float):
        self.X += self.Speed * self.X_dir
        self.Y += self.Speed * self.Y_dir

        self.lifespan += dt

    def draw(self, screen):
        screen.blit(self.Surface, (self.X, self.Y))
