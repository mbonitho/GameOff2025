import math
from pygame import Surface
import pygame

class Bullet:

    def __init__(self, surface: Surface, pos: tuple[int, int], angle_deg: float):
        self.Surface = surface

        self.Rect = surface.get_rect()
        self.RotatedSurface = pygame.transform.rotate(surface, -angle_deg)
        self.Rect = self.RotatedSurface.get_rect(center=self.Rect.center)
        self.Rect.topleft = pos

        angle_rad = math.radians(angle_deg)
        self.X_dir = math.cos(angle_rad)
        self.Y_dir = math.sin(angle_rad)
        
        self.Speed = 18 * 60 # default speed

        self.lifespan = 0
        self.max_lifespan = 0.5 # seconds

    def update(self, enemies, dt: float):
        self.lifespan += dt
        
        self.Rect.x += self.Speed * self.X_dir * dt
        self.Rect.y += self.Speed * self.Y_dir * dt

        for enemy in enemies.copy():
            if self.Rect.colliderect(enemy.Rect):
                self.lifespan = self.max_lifespan # kill bullet
                enemy.ReceiveDamage() # hurt enemy
                if enemy.CurrentLife <= 0:
                    enemies.remove(enemy)


    def draw(self, screen):
        screen.blit(self.RotatedSurface, self.Rect.topleft)
