

from typing import Tuple
import pygame

from gameobjects.enemies.attack_player_in_radius_behavior import AttackPlayerInRadiusBehavior
from gameobjects.enemies.dies_after_a_while_behavior import DiesAfterAWhileBehavior
from gameobjects.enemies.enemy import Enemy
from gameobjects.enemies.flee_players_behavior import FleePlayersBehavior
from gameobjects.enemies.hurt_on_contact_behavior import HurtOnContactBehavior
from gameobjects.enemies.move_randomly_behavior import MoveRandomlyBehavior
from gameobjects.enemies.patrol_behavior import PatrolBehavior
from gameobjects.enemies.seek_nearest_player_behavior import SeekNearestPlayerBehavior
from gameobjects.enemies.shoot_plus_pattern_behavior import ShootPlusPatternBehavior
from gameobjects.enemies.spawn_items_behavior import SpawnItemBehavior
from gameobjects.enemies.summon_minion_behavior import SummonMinionBehavior
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

        enemy = Enemy(surfaces, pos[0], pos[1], [SeekNearestPlayerBehavior(), AttackPlayerInRadiusBehavior()])

        enemy.ScoreValue = 5

        return enemy
    
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

        enemy.ScoreValue = 10

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
        enemy.ScoreValue = 25

        return enemy


    @classmethod
    def GetDistantAntennaTower(cls, pos: Tuple[int, int], angleRange: Tuple[int, int]):


        if 'bulletSurface' not in cls._textures:
            cls._textures['bulletSurface'] = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()

        if 'waveBulletSurface' not in cls._textures:
            cls._textures['waveBulletSurface'] = pygame.image.load('assets/sprites/projectiles/antenna_wave.png').convert_alpha()

        enemy = Enemy([cls._textures['bulletSurface']], pos[0], pos[1], [
                TeleportAndShootWaveBehavior(cls._textures['waveBulletSurface'], angleRange)
            ])
        enemy.ScoreValue = 0
        
        return enemy
    
    @classmethod
    def GetSameRoomAntennaTower(cls, pos: Tuple[int, int]):
        if 'antennaSurface' not in cls._textures:
            cls._textures['antennaSurface'] =pygame.image.load('assets/sprites/objects/antenna.png').convert_alpha()

        enemy = Enemy([cls._textures['antennaSurface']], pos[0], pos[1], [])
        enemy.ScoreValue = 30

        return enemy

    @classmethod
    def GetPlusTurret(cls, pos: Tuple[int, int]):

        if 'turretPlusSurface' not in cls._textures:
            cls._textures['turretPlusSurface'] =pygame.image.load('assets/sprites/enemies/turret_plus.png').convert_alpha()

        if 'waveBulletSurface' not in cls._textures:
            cls._textures['waveBulletSurface'] = pygame.image.load('assets/sprites/projectiles/antenna_wave.png').convert_alpha()

        enemy =  Enemy([cls._textures['turretPlusSurface']], pos[0], pos[1], [
            ShootPlusPatternBehavior(cls._textures['waveBulletSurface'])
        ])
        enemy.MaxLife = 5
        enemy.CurrentLife =  enemy.MaxLife
        enemy.ScoreValue = 15

        return enemy


    @classmethod
    def GetMineDropperEnemy(cls, pos: Tuple[int, int], obstacles: list[pygame.Rect], objects):

        if 'raccoon1' not in cls._textures:
            cls._textures['raccoon1'] = pygame.image.load(f'assets/sprites/enemies/raccoon1.png').convert_alpha()
            cls._textures['raccoon2'] = pygame.image.load(f'assets/sprites/enemies/raccoon2.png').convert_alpha()
            cls._textures['raccoon3'] = pygame.image.load(f'assets/sprites/enemies/raccoon3.png').convert_alpha()

        surfaces = [
            cls._textures['raccoon1'],
            cls._textures['raccoon2'],
            cls._textures['raccoon3']
        ]

        enemy = Enemy(surfaces, pos[0], pos[1], [MoveRandomlyBehavior(obstacles), 
                                                 SpawnItemBehavior(objects, SpawnItemBehavior.ObjectType.MINE)])
    
        enemy.MaxLife = 4
        enemy.CurrentLife =  enemy.MaxLife
        enemy.ScoreValue = 10

        return enemy
    
    @classmethod
    def GetBombDropperEnemy(cls, pos: Tuple[int, int], obstacles: list[pygame.Rect], objects):

        if 'crow1' not in cls._textures:
            cls._textures['crow1'] = pygame.image.load(f'assets/sprites/enemies/crow1.png').convert_alpha()
            cls._textures['crow2'] = pygame.image.load(f'assets/sprites/enemies/crow2.png').convert_alpha()
            cls._textures['crow3'] = pygame.image.load(f'assets/sprites/enemies/crow3.png').convert_alpha()

        surfaces = [
            cls._textures['crow1'],
            cls._textures['crow2'],
            cls._textures['crow3']
        ]

        spawnBehavior = SpawnItemBehavior(objects, SpawnItemBehavior.ObjectType.BOMB)
        spawnBehavior.decisionMinTime = 4
        spawnBehavior.decisionMaxTime = 6

        enemy = Enemy(surfaces, pos[0], pos[1], [MoveRandomlyBehavior(obstacles), 
                                                 spawnBehavior])
    
        enemy.MaxLife = 4
        enemy.CurrentLife =  enemy.MaxLife
        enemy.ScoreValue = 15

        return enemy

    @classmethod
    def GetMiceSummonerEnemy(cls, pos: Tuple[int, int], obstacles: list[pygame.Rect], enemies):

        if 'skunk1' not in cls._textures:
            cls._textures['skunk1'] = pygame.image.load(f'assets/sprites/enemies/skunk1.png').convert_alpha()
            cls._textures['skunk2'] = pygame.image.load(f'assets/sprites/enemies/skunk2.png').convert_alpha()
            cls._textures['skunk3'] = pygame.image.load(f'assets/sprites/enemies/skunk3.png').convert_alpha()

        surfaces = [
            cls._textures['skunk1'],
            cls._textures['skunk2'],
            cls._textures['skunk3']
        ]

        enemy = Enemy(surfaces, pos[0], pos[1], [FleePlayersBehavior(obstacles), 
                                                 SummonMinionBehavior(enemies, SummonMinionBehavior.EnemyType.MOUSE)])
    
        enemy.MaxLife = 4
        enemy.CurrentLife =  enemy.MaxLife
        enemy.ScoreValue = 30

        return enemy
    
    @classmethod
    def GetMoneyDropperEnemy(cls, pos: Tuple[int, int], obstacles: list[pygame.Rect], objects):

        if 'raccoon1' not in cls._textures:
            cls._textures['raccoon1'] = pygame.image.load(f'assets/sprites/enemies/raccoon1.png').convert_alpha()
            cls._textures['raccoon2'] = pygame.image.load(f'assets/sprites/enemies/raccoon2.png').convert_alpha()
            cls._textures['raccoon3'] = pygame.image.load(f'assets/sprites/enemies/raccoon3.png').convert_alpha()

        surfaces = [
            cls._textures['raccoon1'],
            cls._textures['raccoon2'],
            cls._textures['raccoon3']
        ]

        spawnBehavior = SpawnItemBehavior(objects, SpawnItemBehavior.ObjectType.MONEY)
        spawnBehavior.decisionMinTime = 0.25
        spawnBehavior.decisionMaxTime = .6

        moveBehavior = MoveRandomlyBehavior(obstacles)
        moveBehavior.Speed = 220

        enemy = Enemy(surfaces, pos[0], pos[1], [
                                                 DiesAfterAWhileBehavior(5),
                                                 moveBehavior,
                                                 spawnBehavior])
    
        enemy.MaxLife = 20
        enemy.CurrentLife =  enemy.MaxLife
        enemy.ScoreValue = 250

        return enemy

    @classmethod
    def GetPatrollingEnemy(cls, pos: Tuple[int, int], obstacles: list[pygame.Rect], dir: str):

        if 'pigeon1' not in cls._textures:
            cls._textures['pigeon1'] = pygame.image.load(f'assets/sprites/enemies/pigeon1.png').convert_alpha()
            cls._textures['pigeon2'] = pygame.image.load(f'assets/sprites/enemies/pigeon2.png').convert_alpha()
            cls._textures['pigeon3'] = pygame.image.load(f'assets/sprites/enemies/pigeon3.png').convert_alpha()

        surfaces = [
            cls._textures['pigeon1'],
            cls._textures['pigeon2'],
            cls._textures['pigeon3']
        ]

        enemy = Enemy(surfaces, pos[0], pos[1], [PatrolBehavior(obstacles, dir), HurtOnContactBehavior()])
    
        enemy.MaxLife = 8
        enemy.CurrentLife =  enemy.MaxLife
        enemy.ScoreValue = 20

        return enemy