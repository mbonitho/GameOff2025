from pygame import Rect, Surface
from typing import Tuple

import pygame
from gameobjects.blinkingComponent import BlinkingComponent
from utils.helpers.collisions_helper import MoveAndCollide

class Player:

    def __init__(self, index: int, x: int, y: int, color: Tuple[int, int, int]):


        # load surfaces
        self.animations = {
            'walk': [
                pygame.image.load(f'assets/sprites/player/player{index}_walk_0.png').convert_alpha(),
                pygame.image.load(f'assets/sprites/player/player{index}_walk_1.png').convert_alpha(),
                pygame.image.load(f'assets/sprites/player/player{index}_walk_2.png').convert_alpha()],
            'idle': [
                pygame.image.load(f'assets/sprites/player/player{index}_idle_0.png').convert_alpha(),
                pygame.image.load(f'assets/sprites/player/player{index}_idle_0.png').convert_alpha(),
                pygame.image.load(f'assets/sprites/player/player{index}_idle_1.png').convert_alpha()]
        }

        # animation
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = .15 # seconds
        self.looking_right = True
        self.previous_pos = (x, y)

        self.state = 'idle'
        surface = self.animations[self.state][0]

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

        if self.previous_pos == self.Rect.topleft:
            self.state = 'idle'
        else:
            self.state = 'walk'

        # animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer %= self.animation_speed

            self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])

        self.previous_pos = self.Rect.topleft



    def draw(self, screen):
        if self.BlinkingComponent.visible:
            img = self.animations[self.state][self.frame_index]
            if not self.looking_right:
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, self.Rect.topleft)

    def MoveX(self, value, obstacles: list[Rect]):
        MoveAndCollide(self.Rect, self.Speed * value, 0, obstacles)
        self.looking_right = value > 0

    def MoveY(self, value, obstacles: list[Rect]):
        MoveAndCollide(self.Rect, 0, self.Speed * value, obstacles)

    def MoveLeft(self, obstacles: list[Rect], ratio: float = 1):
        MoveAndCollide(self.Rect, int(self.Speed * ratio) * -1, 0, obstacles)
        self.looking_right = False

    def MoveRight(self, obstacles: list[Rect], ratio: float = 1):
        MoveAndCollide(self.Rect, int(self.Speed * ratio), 0, obstacles)
        self.looking_right = True

    def MoveUp(self, obstacles: list[Rect], ratio: float = 1):
        MoveAndCollide(self.Rect, 0, int(self.Speed * ratio) * -1, obstacles)

    def MoveDown(self, obstacles: list[Rect], ratio: float = 1):
        MoveAndCollide(self.Rect, 0, int(self.Speed * ratio), obstacles)

    def ReceiveDamage(self):
        # invicibility fames
        if not self.BlinkingComponent.IsBlinking():
            self.BlinkingComponent.StartBlinking()
            self.CurrentLife -= 1

    def TryShootBullet(self, bullet):

        if len(self.Bullets) < self.MaxBullets:
            self.Bullets.append(bullet)

        self.looking_right = bullet.X_dir > 0
