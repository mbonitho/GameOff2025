

from typing import Tuple
import pygame

from gameobjects.enemies.attack_player_in_radius_behavior import AttackPlayerInRadiusBehavior
from gameobjects.enemies.enemy import Enemy
from gameobjects.enemies.flee_players_behavior import FleePlayersBehavior
from gameobjects.enemies.move_randomly_behavior import MoveRandomlyBehavior
from gameobjects.enemies.seek_nearest_player_behavior import SeekNearestPlayerBehavior
from gameobjects.enemies.shoot_plus_pattern_behavior import ShootPlusPatternBehavior
from gameobjects.enemies.spawn_Mines_behavior import SpawnMineBehavior
from gameobjects.enemies.teleport_and_shoot_wave_behavior import TeleportAndShootWaveBehavior


class EnemyFactory:

    _textures = {}

    @classmethod
    def GetDefaultEnemy(cls, pos: Tuple[int, int]):

        if 'enemy_red_0' not in cls._textures:
            cls._textures['enemy_red_0'] = pygame.image.load(f'assets/sprites/enemies/enemy_red_0.png').convert_alpha()
            cls._textures['enemy_red_1'] = pygame.image.load(f'assets/sprites/enemies/enemy_red_1.png').convert_alpha()
            cls._textures['enemy_red_2'] = pygame.image.load(f'assets/sprites/enemies/enemy_red_2.png').convert_alpha()

        surfaces = [
            cls._textures['enemy_red_0'],
            cls._textures['enemy_red_1'],
            cls._textures['enemy_red_2']
        ]

        return Enemy(surfaces, pos[0], pos[1], [SeekNearestPlayerBehavior(), AttackPlayerInRadiusBehavior()])
    

    @classmethod
    def GetDistantAntennaTower(cls, pos: Tuple[int, int], angleRange: Tuple[int, int]):


        if 'bulletSurface' not in cls._textures:
            cls._textures['bulletSurface'] = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()

        if 'waveBulletSurface' not in cls._textures:
            cls._textures['waveBulletSurface'] = pygame.image.load('assets/sprites/projectiles/antenna_wave.png').convert_alpha()

        return Enemy([cls._textures['bulletSurface']], pos[0], pos[1], [
                TeleportAndShootWaveBehavior(cls._textures['waveBulletSurface'], angleRange)
            ])
    
    @classmethod
    def GetSameRoomAntennaTower(cls, pos: Tuple[int, int]):
        if 'antennaSurface' not in cls._textures:
            cls._textures['antennaSurface'] =pygame.image.load('assets/sprites/objects/antenna.png').convert_alpha()

        return  Enemy([cls._textures['antennaSurface']], pos[0], pos[1], [])


    @classmethod
    def GetPlusTurret(cls, pos: Tuple[int, int]):

        if 'turretPlusSurface' not in cls._textures:
            cls._textures['turretPlusSurface'] =pygame.image.load('assets/sprites/enemies/turret_plus.png').convert_alpha()

        if 'waveBulletSurface' not in cls._textures:
            cls._textures['waveBulletSurface'] = pygame.image.load('assets/sprites/projectiles/antenna_wave.png').convert_alpha()

        turret =  Enemy([cls._textures['turretPlusSurface']], pos[0], pos[1], [
            ShootPlusPatternBehavior(cls._textures['waveBulletSurface'])
        ])

        turret.MaxLife = 5
        turret.CurrentLife =  turret.MaxLife

        return turret


    @classmethod
    def GetMineDropperEnemy(cls, pos: Tuple[int, int], obstacles, objects):

        if 'raccoon1' not in cls._textures:
            cls._textures['raccoon1'] = pygame.image.load(f'assets/sprites/enemies/raccoon1.png').convert_alpha()
            cls._textures['raccoon2'] = pygame.image.load(f'assets/sprites/enemies/raccoon2.png').convert_alpha()
            cls._textures['raccoon3'] = pygame.image.load(f'assets/sprites/enemies/raccoon3.png').convert_alpha()

        surfaces = [
            cls._textures['raccoon1'],
            cls._textures['raccoon2'],
            cls._textures['raccoon3']
        ]

        enemy = Enemy(surfaces, pos[0], pos[1], [MoveRandomlyBehavior(obstacles), SpawnMineBehavior(objects)])
    
        enemy.MaxLife = 4
        enemy.CurrentLife =  enemy.MaxLife

        return enemy