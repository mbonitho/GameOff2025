from typing import Tuple
import pygame

from gameobjects.weapons.weapon import Weapon

class WeaponFactory:

    _textures = {}

    @classmethod
    def GetDefaultWeapon(cls, owner):

        if 'weapon1' not in cls._textures: 
            cls._textures['weapon1'] = pygame.image.load(f'assets/sprites/objects/defaultGun.png').convert_alpha()

        if 'bullet1' not in cls._textures:
            cls._textures['bullet1'] = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()

        wpnSurface = cls._textures['weapon1']
        bulletSurface = cls._textures['bullet1']

        weapon = Weapon(owner, wpnSurface, bulletSurface)

        return weapon
    
    @classmethod
    def GetLv1Shotgun(cls, owner):

        if 'weapon1' not in cls._textures: #todo correct texture for weapon
            cls._textures['weapon1'] = pygame.image.load(f'assets/sprites/objects/defaultGun.png').convert_alpha()

        if 'bullet1' not in cls._textures:
            cls._textures['bullet1'] = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()

        wpnSurface = cls._textures['weapon1']
        bulletSurface = cls._textures['bullet1']

        weapon = Weapon(owner, wpnSurface, bulletSurface)
        weapon.Angles = {
            'l': [165,180,195],
            'r': [-15,0,15],
            'u': [255,270,285],
            'd': [75,90,105]
        }
        weapon.TotalAmunition = 30

        return weapon
    
    @classmethod
    def GetLv2Shotgun(cls, owner):

        if 'defaultGun' not in cls._textures: #todo correct texture for weapon
            cls._textures['defaultGun'] = pygame.image.load(f'assets/sprites/objects/defaultGun.png').convert_alpha()

        if 'bullet1' not in cls._textures:
            cls._textures['bullet1'] = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()

        wpnSurface = cls._textures['weapon1']
        bulletSurface = cls._textures['bullet1']

        weapon = Weapon(owner, wpnSurface, bulletSurface)
        weapon.Angles = {
            'l': [150,165,180,195, 210],
            'r': [-30,-15,0,15,30],
            'u': [240,255,270,285,300],
            'd': [60,75,90,105,120]
        }
        weapon.TotalAmunition = 20

        return weapon
