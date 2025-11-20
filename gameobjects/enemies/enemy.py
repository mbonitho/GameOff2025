from typing import List
from pygame import Surface
import pygame
from gameobjects.blinkingComponent import BlinkingComponent
from gameobjects.enemies.enemy_behavior import EnemyBehavior

class Enemy:
    def __init__(self, surfaces: List[Surface], x: int, y: int, behaviors: list[EnemyBehavior]):     

        self.animations = surfaces

        # animation
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = .15 # seconds
        self.looking_right = True
        self.previous_pos = (x, y)

        self.Surface = self.animations[0]
        self.Rect = self.Surface.get_rect()
        self.Rect.topleft = (x, y)
        self.Behaviors = behaviors

        self.BlinkingComponent = BlinkingComponent()
        self.BlinkingComponent.total_blinking_duration = 0.3 # seconds

        self.MaxLife = 2
        self.CurrentLife =  self.MaxLife

        self.KilledByPlayerIndex: int | None = None
        self.ScoreValue = 10

        self.Scale = 1
        self.IsABoss = False

    def update(self, players, dt: float):
        self.BlinkingComponent.update(dt)

        self.looking_right = self.previous_pos[0] < self.Rect.x

        # animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer %= self.animation_speed
            self.frame_index = (self.frame_index + 1) % len(self.animations)

        self.previous_pos = self.Rect.topleft
        for beh in self.Behaviors:
            beh.update(self, players, dt)


    def draw(self, screen):
        if self.BlinkingComponent.visible:

            img = self.animations[self.frame_index]
            if not self.looking_right:
                img = pygame.transform.flip(img, True, False)

            if self.Scale > 1:
                img = pygame.transform.scale(img, (img.get_width() * self.Scale, img.get_height() * self.Scale))

            screen.blit(img, self.Rect.topleft)

            for beh in self.Behaviors:
                beh.draw(screen, self)

    def ReceiveDamage(self, playerIndex:  int):
        if not self.BlinkingComponent.IsBlinking():
            self.BlinkingComponent.StartBlinking()
            self.CurrentLife -= 1
            self.KilledByPlayerIndex = playerIndex

