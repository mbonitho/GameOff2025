import math

import pygame
from gameobjects.enemies.enemy_behavior import EnemyBehavior

class AttackPlayerInRadiusBehavior(EnemyBehavior):

    def __init__(self, damage: int = 1, radius: int = 144):
        super().__init__()
        self.attack_radius = radius
        self.in_attack_range = False

        self.contact_timers = {}  # player -> time in contact
        self.attack_cooldown = .75  # seconds before damage

        self.damage = damage

    def update(self, enemy, players, dt):
        # hurt players that stay too long in attack range
        for player in players:
            dx = player.Rect.x - enemy.Rect.x
            dy = player.Rect.y - enemy.Rect.y
            dist = math.hypot(dx, dy)

            self.in_attack_range = dist <= self.attack_radius

            if dist <= self.attack_radius:
                # Player is in contact
                self.contact_timers[player] = self.contact_timers.get(player, 0) + dt

                if self.contact_timers[player] >= self.attack_cooldown:
                    player.ReceiveDamage(self.damage)
                    self.contact_timers[player] = 0  # reset after damage
            else:
                # Player left the zone
                self.contact_timers[player] = 0

    def draw(self, screen, enemy):
        if self.in_attack_range:
            # Draw red semi-transparent circle
            overlay = pygame.Surface((self.attack_radius * 2, self.attack_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (255, 0, 0, 100), (self.attack_radius, self.attack_radius), self.attack_radius)
            screen.blit(overlay, (enemy.Rect.x + enemy.Rect.width // 2 - self.attack_radius,
                                  enemy.Rect.y + enemy.Rect.height // 2 - self.attack_radius))