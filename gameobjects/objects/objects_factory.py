from typing import Tuple
import pygame

from gameobjects.objects.landmine import Landmine
from gameobjects.objects.medkit import Medkit


class ObjectsFactory:

    _textures = {}
    
    @classmethod
    def GetMedkit(cls, pos: Tuple[int, int]):
        if 'medkit' not in cls._textures:
            cls._textures['medkit'] =pygame.image.load('assets/sprites/objects/medkit.png').convert_alpha()

        return  Medkit(cls._textures['medkit'], pos[0], pos[1])

    @classmethod
    def GetLandmine(cls, pos: Tuple[int, int]):
        if 'landmine' not in cls._textures:
            cls._textures['landmine'] =pygame.image.load('assets/sprites/objects/landmine.png').convert_alpha()

        return  Landmine(cls._textures['landmine'], pos[0], pos[1])
   