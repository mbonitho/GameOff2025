from typing import Tuple
import pygame

from gameobjects.weapons.weapon import Weapon

class WeaponFactory:

    _textures = {}

    @classmethod
    def GetDefaultWeapon(cls, owner):

        if 'defaultGun' not in cls._textures: 
            cls._textures['defaultGun'] = pygame.image.load(f'assets/sprites/objects/defaultGun.png').convert_alpha()

        if 'bullet1' not in cls._textures:
            cls._textures['bullet1'] = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()

        wpnSurface = cls._textures['defaultGun']
        bulletSurface = cls._textures['bullet1']

        weapon = Weapon(owner, wpnSurface, bulletSurface)

        return weapon
    
    @classmethod
    def GetUzi(cls, owner):

        if 'uzi' not in cls._textures: 
            cls._textures['uzi'] = pygame.image.load(f'assets/sprites/objects/uzi.png').convert_alpha()

        if 'bullet1' not in cls._textures:
            cls._textures['bullet1'] = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()

        wpnSurface = cls._textures['uzi']
        bulletSurface = cls._textures['bullet1']

        weapon = Weapon(owner, wpnSurface, bulletSurface)
        weapon.BulletSpeed = int(weapon.BulletSpeed * 2)
        weapon.BulletMaxLifespan *= 2
        weapon.TotalAmunition = 300
        weapon.MaxBulletsOnScreen = 15

        return weapon
    
    @classmethod
    def GetLv1Shotgun(cls, owner):

        if 'musket' not in cls._textures: #todo correct texture for weapon
            cls._textures['musket'] = pygame.image.load(f'assets/sprites/objects/musket.png').convert_alpha()

        if 'bullet1' not in cls._textures:
            cls._textures['bullet1'] = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()

        wpnSurface = cls._textures['musket']
        bulletSurface = cls._textures['bullet1']

        weapon = Weapon(owner, wpnSurface, bulletSurface)
        weapon.Angles = {
            'l': [165,180,195],
            'r': [-15,0,15],
            'u': [255,270,285],
            'd': [75,90,105]
        }
        weapon.BulletSpeed = int(weapon.BulletSpeed * .75)
        weapon.BulletMaxLifespan = 0.25
        weapon.TotalAmunition = 50
        weapon.BulletDamage = 1

        return weapon
    
    @classmethod
    def GetLv2Shotgun(cls, owner):

        if 'shotgun' not in cls._textures: #todo correct texture for weapon
            cls._textures['shotgun'] = pygame.image.load(f'assets/sprites/objects/shotgun.png').convert_alpha()

        if 'bullet1' not in cls._textures:
            cls._textures['bullet1'] = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()

        wpnSurface = cls._textures['shotgun']
        bulletSurface = cls._textures['bullet1']

        weapon = Weapon(owner, wpnSurface, bulletSurface)
        weapon.Angles = {
            'l': [150,165,180,195, 210],
            'r': [-30,-15,0,15,30],
            'u': [240,255,270,285,300],
            'd': [60,75,90,105,120]
        }
        weapon.BulletSpeed = int(weapon.BulletSpeed * .75)
        weapon.BulletMaxLifespan = 0.25
        weapon.TotalAmunition = 30
        weapon.BulletDamage = 1
        
        return weapon
