import math
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

        self.contact_timers = {}  # player -> time in contact
        self.attack_cooldown = 1.0  # seconds before damage


    def update(self, players, dt: float):
        for beh in self.Behaviors:
            beh.update(self, players, dt)

        # hurt players that stay too long in attack range
        for player in players:
            dx = player.Rect.x - self.Rect.x
            dy = player.Rect.y - self.Rect.y
            dist = math.hypot(dx, dy)

            if dist <= self.attack_radius:
                # Player is in contact
                self.contact_timers[player] = self.contact_timers.get(player, 0) + dt

                if self.contact_timers[player] >= self.attack_cooldown:
                    player.ReceiveDamage()
                    self.contact_timers[player] = 0  # reset after damage
            else:
                # Player left the zone
                self.contact_timers[player] = 0

    def draw(self, screen):
        screen.blit(self.Surface, self.Rect.topleft)

        if self.in_attack_range:
            # Draw red semi-transparent circle
            overlay = pygame.Surface((self.attack_radius * 2, self.attack_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (255, 0, 0, 100), (self.attack_radius, self.attack_radius), self.attack_radius)
            screen.blit(overlay, (self.Rect.x + self.Rect.width // 2 - self.attack_radius,
                                  self.Rect.y + self.Rect.height // 2 - self.attack_radius))
