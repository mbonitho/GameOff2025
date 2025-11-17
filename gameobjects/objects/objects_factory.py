

from typing import Tuple
import pygame
from pygame import Surface

from gameobjects.enemies.attack_player_in_radius_behavior import AttackPlayerInRadiusBehavior
from gameobjects.enemies.enemy import Enemy
from gameobjects.enemies.seek_nearest_player_behavior import SeekNearestPlayerBehavior
from gameobjects.enemies.shoot_plus_pattern_behavior import ShootPlusPatternBehavior
from gameobjects.enemies.teleport_and_shoot_wave_behavior import TeleportAndShootWaveBehavior
from gameobjects.objects.medkit import Medkit


class ObjectsFactory:

    _textures = {}
    
    @classmethod
    def GetMedkit(cls, pos: Tuple[int, int]):
        if 'medkit' not in cls._textures:
            cls._textures['medkit'] =pygame.image.load('assets/sprites/objects/medkit.png').convert_alpha()

        return  Medkit(cls._textures['medkit'], pos[0], pos[1])


   