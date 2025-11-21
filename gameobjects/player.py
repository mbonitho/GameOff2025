from pygame import Rect, Surface
from typing import Tuple

import pygame
from gameobjects.blinkingComponent import BlinkingComponent
from gameobjects.bullet import Bullet
from utils.helpers.collisions_helper import MoveAndCollide

class Player:


    def __init__(self, index: int, x: int, y: int):

        # load surfaces
        self.bulletTexture = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()
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

        self.Speed = 6
        self.MaxLife = 5
        self.CurrentLife = self.MaxLife
        self.Score = 0

        self.WeaponLevel = 1
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

    def ReceiveDamage(self, dmg: int = 1):
        # invicibility fames
        if not self.BlinkingComponent.IsBlinking():
            self.BlinkingComponent.StartBlinking()
            self.CurrentLife -= dmg
            return True
        return False

    def TryShootBullet(self, direction: str):

        factor = 1
        if self.WeaponLevel == 2:
            factor = 3
        elif self.WeaponLevel == 3:
            factor = 5

        if len(self.Bullets) >= self.MaxBullets * factor:
            return

        origin = (-1,-1)
        angles= []

        match direction:

            case 'l':
                origin = self.Rect.midleft
                match self.WeaponLevel:
                    case 1:
                        angles = [180]
                    case 2:
                        angles = [165,180,195]
                    case 3:
                        angles = [150,165,180,195, 210]

            case 'r':
                origin = self.Rect.midright
                match self.WeaponLevel:
                    case 1:
                        angles = [0]
                    case 2:
                        angles = [-15,0,15]
                    case 3:
                        angles = [-30,-15,0,15,30]

            case 'u':
                origin = self.Rect.midtop
                match self.WeaponLevel:
                    case 1:
                        angles = [270]
                    case 2:
                        angles = [255,270,285]
                    case 3:
                        angles = [240,255,270,285,300]

            case 'd':
                origin = self.Rect.midbottom
                match self.WeaponLevel:
                    case 1:
                        angles = [90]
                    case 2:
                        angles = [75,90,105]
                    case 3:
                        angles = [60,75,90,105,120]

        for angle in angles:
            bullet = Bullet(self.bulletTexture, origin, angle)
            self.Bullets.append(bullet)
            self.looking_right = bullet.X_dir > 0
