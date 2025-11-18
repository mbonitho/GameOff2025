

from typing import Tuple
import pygame

from gameobjects.enemies.attack_player_in_radius_behavior import AttackPlayerInRadiusBehavior
from gameobjects.enemies.enemy import Enemy
from gameobjects.enemies.flee_players_behavior import FleePlayersBehavior
from gameobjects.enemies.move_randomly_behavior import MoveRandomlyBehavior
from gameobjects.enemies.seek_nearest_player_behavior import SeekNearestPlayerBehavior
from gameobjects.enemies.shoot_plus_pattern_behavior import ShootPlusPatternBehavior
from gameobjects.enemies.spawn_Mines_behavior import SpawnMineBehavior
from gameobjects.enemies.summon_mice_behavior import SummonMiceBehavior
from gameobjects.enemies.teleport_and_shoot_wave_behavior import TeleportAndShootWaveBehavior


class EnemyFactory:

    _textures = {}

    @classmethod
    def GetDefaultEnemy(cls, pos: Tuple[int, int]):

        if 'rabbit1' not in cls._textures:
            cls._textures['rabbit1'] = pygame.image.load(f'assets/sprites/enemies/rabbit1.png').convert_alpha()
            cls._textures['rabbit2'] = pygame.image.load(f'assets/sprites/enemies/rabbit2.png').convert_alpha()
            cls._textures['rabbit3'] = pygame.image.load(f'assets/sprites/enemies/rabbit3.png').convert_alpha()

        surfaces = [
            cls._textures['rabbit1'],
            cls._textures['rabbit2'],
            cls._textures['rabbit3']
        ]

        return Enemy(surfaces, pos[0], pos[1], [SeekNearestPlayerBehavior(), AttackPlayerInRadiusBehavior()])
    
    @classmethod
    def GetSmallFastEnemy(cls, pos: Tuple[int, int]):

        if 'mouse1' not in cls._textures:
            cls._textures['mouse1'] = pygame.image.load(f'assets/sprites/enemies/mouse1.png').convert_alpha()
            cls._textures['mouse2'] = pygame.image.load(f'assets/sprites/enemies/mouse2.png').convert_alpha()
            cls._textures['mouse3'] = pygame.image.load(f'assets/sprites/enemies/mouse3.png').convert_alpha()

        surfaces = [
            cls._textures['mouse1'],
            cls._textures['mouse2'],
            cls._textures['mouse3']
        ]

        seekBehavior = SeekNearestPlayerBehavior()
        seekBehavior.Speed = 140

        enemy =  Enemy(surfaces, pos[0], pos[1], [seekBehavior, AttackPlayerInRadiusBehavior()])

        enemy.MaxLife = 2
        enemy.CurrentLife = enemy.MaxLife

        return enemy


    @classmethod
    def GetBigSlowEnemy(cls, pos: Tuple[int, int]):

        if 'bear1' not in cls._textures:
            cls._textures['bear1'] = pygame.image.load(f'assets/sprites/enemies/bear1.png').convert_alpha()
            cls._textures['bear2'] = pygame.image.load(f'assets/sprites/enemies/bear2.png').convert_alpha()
            cls._textures['bear3'] = pygame.image.load(f'assets/sprites/enemies/bear3.png').convert_alpha()

        surfaces = [
            cls._textures['bear1'],
            cls._textures['bear2'],
            cls._textures['bear3']
        ]

        seekBehavior = SeekNearestPlayerBehavior()
        seekBehavior.Speed = 70

        enemy =  Enemy(surfaces, pos[0], pos[1], [seekBehavior, AttackPlayerInRadiusBehavior()])

        enemy.MaxLife = 5
        enemy.CurrentLife = enemy.MaxLife

        return enemy


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
    

    @classmethod
    def GetMiceSummonerEnemy(cls, pos: Tuple[int, int], obstacles, enemies):

        if 'skunk1' not in cls._textures:
            cls._textures['skunk1'] = pygame.image.load(f'assets/sprites/enemies/skunk1.png').convert_alpha()
            cls._textures['skunk2'] = pygame.image.load(f'assets/sprites/enemies/skunk2.png').convert_alpha()
            cls._textures['skunk3'] = pygame.image.load(f'assets/sprites/enemies/skunk3.png').convert_alpha()

        surfaces = [
            cls._textures['skunk1'],
            cls._textures['skunk2'],
            cls._textures['skunk3']
        ]

        enemy = Enemy(surfaces, pos[0], pos[1], [FleePlayersBehavior(obstacles), SummonMiceBehavior(enemies)])
    
        enemy.MaxLife = 4
        enemy.CurrentLife =  enemy.MaxLife

        return enemy