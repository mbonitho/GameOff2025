import pygame
from pygame import Rect

from gameobjects.blinkingComponent import BlinkingComponent
from gameobjects.weapons.weapons_factory import WeaponFactory
from utils.helpers.collisions_helper import MoveAndCollide

class Player:

    def __init__(self, index: int, x: int, y: int):

        self.playerIndex = index

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

        self.Lives = 3
        self.Speed = 6
        self.MaxLife = 5
        self.CurrentLife = self.MaxLife
        self.Score = 0

        self.Weapon = WeaponFactory.GetDefaultWeapon(self)

        self.BlinkingComponent = BlinkingComponent()

    def initializeWeapon(self):
        self.Weapon = WeaponFactory.GetDefaultWeapon(self)
    
    def update(self, enemies: list, dt: float):

        if self.CurrentLife <= 0:
            return
        
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

        # weapon
        self.Weapon.update(enemies, dt)

        self.previous_pos = self.Rect.topleft

    def draw(self, screen):

        if self.CurrentLife <= 0:
            return

        if self.BlinkingComponent.visible:
            img = self.animations[self.state][self.frame_index]
            if not self.looking_right:
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, self.Rect.topleft)

        self.Weapon.draw(screen)

    def MoveX(self, value, obstacles: list[Rect]):
        if self.CurrentLife <= 0:
            return
        MoveAndCollide(self.Rect, self.Speed * value, 0, obstacles)
        self.looking_right = value > 0

    def MoveY(self, value, obstacles: list[Rect]):
        if self.CurrentLife <= 0:
            return
        MoveAndCollide(self.Rect, 0, self.Speed * value, obstacles)

    def MoveLeft(self, obstacles: list[Rect], ratio: float = 1):
        if self.CurrentLife <= 0:
            return
        MoveAndCollide(self.Rect, int(self.Speed * ratio) * -1, 0, obstacles)
        self.looking_right = False

    def MoveRight(self, obstacles: list[Rect], ratio: float = 1):
        if self.CurrentLife <= 0:
            return
        MoveAndCollide(self.Rect, int(self.Speed * ratio), 0, obstacles)
        self.looking_right = True

    def MoveUp(self, obstacles: list[Rect], ratio: float = 1):
        if self.CurrentLife <= 0:
            return
        MoveAndCollide(self.Rect, 0, int(self.Speed * ratio) * -1, obstacles)

    def MoveDown(self, obstacles: list[Rect], ratio: float = 1):
        if self.CurrentLife <= 0:
            return
        MoveAndCollide(self.Rect, 0, int(self.Speed * ratio), obstacles)

    def ReceiveDamage(self, dmg: int = 1):
        # invicibility fames
        if not self.BlinkingComponent.IsBlinking():
            self.BlinkingComponent.StartBlinking()
            self.CurrentLife -= dmg
            return True
        return False

    def TryShootBullet(self, direction: str):
        if self.CurrentLife <= 0:
            return
        self.Weapon.TryShootBullet(direction)
