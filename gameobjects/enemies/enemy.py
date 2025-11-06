import pygame
from pygame import Surface

from gameobjects.enemies.enemy_behavior import EnemyBehavior

class Enemy:
    def __init__(self, surface: Surface, x: int, y: int, behaviors: list[EnemyBehavior]):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)
        self.Speed = 100
        self.Behaviors = behaviors

        self.attack_radius = 72
        self.in_attack_range = False

    def update(self, players, dt: float):
        for beh in self.Behaviors:
            beh.update(self, players, dt)

    def draw(self, screen):
        screen.blit(self.Surface, self.Rect.topleft)

        if self.in_attack_range:
            # Draw red semi-transparent circle
            overlay = pygame.Surface((self.attack_radius * 2, self.attack_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (255, 0, 0, 100), (self.attack_radius, self.attack_radius), self.attack_radius)
            screen.blit(overlay, (self.Rect.x + self.Rect.width // 2 - self.attack_radius,
                                  self.Rect.y + self.Rect.height // 2 - self.attack_radius))
