import pygame
from gameobjects.enemies.enemy_behavior import EnemyBehavior

class EvolutiveBehavior(EnemyBehavior):

    def __init__(self, obstacles: list[pygame.Rect], objects: list, enemies: list):
        super().__init__()

        self.obstacles = obstacles
        self.objects = objects
        self.enemies = enemies

        self.nextBehaviorThreshold: float = 1

    def update(self, enemy, players, dt):

        if enemy.CurrentLife <= enemy.MaxLife * self.nextBehaviorThreshold:
            enemy.behaviors = [self]

            match self.nextBehaviorThreshold :
                
                ####################################
                # 1st stage: default enemy
                ####################################
                case 1: 
                    from gameobjects.enemies.seek_nearest_player_behavior import SeekNearestPlayerBehavior
                    seekBehavior = SeekNearestPlayerBehavior()
                    seekBehavior.Speed = 160
                    enemy.Behaviors.append(seekBehavior)

                    from gameobjects.enemies.attack_player_in_radius_behavior import AttackPlayerInRadiusBehavior
                    atkRadiusBehavior = AttackPlayerInRadiusBehavior(2, 200)
                    enemy.Behaviors.append(atkRadiusBehavior)
                    

                ####################################
                # 2nd stage: mines and hurt on contact
                ####################################
                case 0.75: 
                    from gameobjects.enemies.move_randomly_behavior import MoveRandomlyBehavior
                    moveRandmonly = MoveRandomlyBehavior(self.obstacles)
                    moveRandmonly.Speed = 240
                    enemy.Behaviors.append(moveRandmonly)
                    
                    from gameobjects.enemies.hurt_on_contact_behavior import HurtOnContactBehavior
                    hurtOnContact = HurtOnContactBehavior()
                    hurtOnContact.damage = 1
                    enemy.Behaviors.append(hurtOnContact)

                    from gameobjects.enemies.spawn_items_behavior import SpawnItemBehavior
                    spawnBehavior = SpawnItemBehavior(self.objects, SpawnItemBehavior.ObjectType.MINE)
                    spawnBehavior.decisionMinTime = 1
                    spawnBehavior.decisionMaxTime = 3
                    enemy.Behaviors.append(spawnBehavior)

                ####################################
                # 3rd stage: mines and bombs and hurt on contact
                ####################################
                case 0.5: 
                    from gameobjects.enemies.move_randomly_behavior import MoveRandomlyBehavior
                    moveRandmonly = MoveRandomlyBehavior(self.obstacles)
                    moveRandmonly.Speed = 220
                    enemy.Behaviors.append(moveRandmonly)
                    
                    from gameobjects.enemies.hurt_on_contact_behavior import HurtOnContactBehavior
                    hurtOnContact = HurtOnContactBehavior()
                    hurtOnContact.damage = 1
                    enemy.Behaviors.append(hurtOnContact)

                    from gameobjects.enemies.spawn_items_behavior import SpawnItemBehavior
                    spawnMineBehavior = SpawnItemBehavior(self.objects, SpawnItemBehavior.ObjectType.MINE)
                    spawnMineBehavior.decisionMinTime = 1
                    spawnMineBehavior.decisionMaxTime = 3
                    enemy.Behaviors.append(spawnMineBehavior)

                    spawnBombBehavior = SpawnItemBehavior(self.objects, SpawnItemBehavior.ObjectType.BOMB)
                    spawnBombBehavior.decisionMinTime = 1
                    spawnBombBehavior.decisionMaxTime = 3
                    enemy.Behaviors.append(spawnBombBehavior)


                ####################################
                # 4th and final stage:
                ####################################
                case 0.25: 
                    from gameobjects.enemies.move_randomly_behavior import MoveRandomlyBehavior
                    moveRandmonly = MoveRandomlyBehavior(self.obstacles)
                    moveRandmonly.Speed = 200
                    enemy.Behaviors.append(moveRandmonly)
                    
                    from gameobjects.enemies.hurt_on_contact_behavior import HurtOnContactBehavior
                    hurtOnContact = HurtOnContactBehavior()
                    hurtOnContact.damage = 1
                    enemy.Behaviors.append(hurtOnContact)

                    from gameobjects.enemies.spawn_items_behavior import SpawnItemBehavior
                    spawnMineBehavior = SpawnItemBehavior(self.objects, SpawnItemBehavior.ObjectType.MINE)
                    spawnMineBehavior.decisionMinTime = 1
                    spawnMineBehavior.decisionMaxTime = 3
                    enemy.Behaviors.append(spawnMineBehavior)

                    spawnBombBehavior = SpawnItemBehavior(self.objects, SpawnItemBehavior.ObjectType.BOMB)
                    spawnBombBehavior.decisionMinTime = 1
                    spawnBombBehavior.decisionMaxTime = 3
                    enemy.Behaviors.append(spawnBombBehavior)

                    from gameobjects.enemies.summon_minion_behavior import SummonMinionBehavior
                    summonBehavior = SummonMinionBehavior(self.enemies, SummonMinionBehavior.EnemyType.MOUSE)
                    enemy.Behaviors.append(summonBehavior)

            self.nextBehaviorThreshold -= 0.25


    def draw(self, screen, enemy):
        pass