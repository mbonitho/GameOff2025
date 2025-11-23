import random
from typing import Tuple
import pygame

from gameobjects.objects.bomb import Bomb
from gameobjects.objects.explosion import Explosion
from gameobjects.objects.helpButton import HelpButton
from gameobjects.objects.landmine import Landmine
from gameobjects.objects.maxlifeup import MaxLifeUp
from gameobjects.objects.medkit import Medkit
from gameobjects.objects.moneyBag import MoneyBag
from gameobjects.objects.vendingmachine import VendingMachine
from gameobjects.objects.weapon_pickup import WeaponPickup

class ObjectsFactory:

    _textures = {}
    
    @classmethod
    def GetMedkit(cls, pos: Tuple[int, int]):
        if 'medkit' not in cls._textures:
            cls._textures['medkit'] = pygame.image.load('assets/sprites/objects/medkit.png').convert_alpha()

        return  Medkit(cls._textures['medkit'], pos[0], pos[1])

    @classmethod
    def GetMoneyBag(cls, pos: Tuple[int, int], value: int):
        if 'moneybag' not in cls._textures:
            cls._textures['moneybag'] = pygame.image.load('assets/sprites/objects/moneyBag.png').convert_alpha()

        return  MoneyBag(cls._textures['moneybag'], pos[0], pos[1], value)

    @classmethod
    def GetMaxLifeUp(cls, pos: Tuple[int, int], value: int):
        if 'maxlifeUp' not in cls._textures:
            cls._textures['maxlifeUp'] = pygame.image.load('assets/sprites/objects/maxlifeUp.png').convert_alpha()

        return  MaxLifeUp(cls._textures['maxlifeUp'], pos[0], pos[1], value)

    @classmethod
    def GetLandmine(cls, pos: Tuple[int, int]):
        if 'landmine' not in cls._textures:
            cls._textures['landmine'] = pygame.image.load('assets/sprites/objects/landmine.png').convert_alpha()

        return  Landmine(cls._textures['landmine'], pos[0], pos[1])
   
    @classmethod
    def GetExplosion(cls, pos: Tuple[int, int]):
        if 'explosion' not in cls._textures:
            cls._textures['explosion'] = pygame.image.load('assets/sprites/objects/explosion.png').convert_alpha()

        return  Explosion(cls._textures['explosion'], pos[0], pos[1])

    @classmethod
    def GetBomb(cls, pos: Tuple[int, int], objects):
        if 'bomb' not in cls._textures:
            cls._textures['bomb'] = pygame.image.load('assets/sprites/objects/bomb.png').convert_alpha()
        if 'bomb_red' not in cls._textures:
            cls._textures['bomb_red'] = pygame.image.load('assets/sprites/objects/bomb_red.png').convert_alpha()

        return  Bomb([cls._textures['bomb'], cls._textures['bomb_red']], pos[0], pos[1], objects)
    
    @classmethod
    def GetHelpButton(cls, pos: Tuple[int, int], textkey: str):
        if 'helpButton' not in cls._textures:
            cls._textures['helpButton'] = pygame.image.load('assets/sprites/objects/helpButton.png').convert_alpha()

        return  HelpButton(cls._textures['helpButton'], pos[0], pos[1], textkey)
    
    @classmethod
    def GetVendingMachine(cls, pos: Tuple[int, int]):
        if 'vendingMachine' not in cls._textures:
            cls._textures['vendingMachine'] = pygame.image.load('assets/sprites/objects/vendingMachine.png').convert_alpha()

        return  VendingMachine(cls._textures['vendingMachine'], pos[0], pos[1])

    @classmethod
    def GetRandomWeaponPickup(cls, pos: Tuple[int, int]):
        from gameobjects.weapons.weapons_factory import WeaponFactory
        wpnTypes = ['lv1Shotgun', 'lv2Shotgun', 'uzi']

        match random.choice(wpnTypes):

            case 'lv1Shotgun':
                wpn = WeaponFactory.GetLv1Shotgun(None)

            case 'lv2Shotgun':
                wpn = WeaponFactory.GetLv2Shotgun(None)

            case 'uzi':
                wpn = WeaponFactory.GetUzi(None)

        weaponPickup = WeaponPickup(wpn.WeaponSurface, pos[0], pos[1], wpn)

        return weaponPickup
