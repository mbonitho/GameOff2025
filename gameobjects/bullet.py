from pygame import Surface
import pygame

class Bullet:

    def __init__(self, surface: Surface, pos: tuple[int, int], x_dir: int, y_dir: int):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = pos
        self.X_dir = x_dir
        self.Y_dir = y_dir
        
        self.Speed = 18 # default speed

        self.lifespan = 0
        self.max_lifespan = 0.2 # seconds

    def update(self, enemies, dt: float):
        self.lifespan += dt
        
        self.Rect.x += self.Speed * self.X_dir
        self.Rect.y += self.Speed * self.Y_dir

        for enemy in enemies.copy():
            if self.Rect.colliderect(enemy.Rect):
                enemies.remove(enemy)
                self.lifespan = self.max_lifespan


    def draw(self, screen):
        screen.blit(self.Surface, self.Rect.topleft)
