
import random
import pygame
from pygame.locals import *

from gameobjects.blinking_text import BlinkingText
from gameobjects.bullet import Bullet
from gameobjects.enemies.attack_player_in_radius_behavior import AttackPlayerInRadiusBehavior
from gameobjects.enemies.seek_nearest_player_behavior import SeekNearestPlayerBehavior
from gameobjects.level import Level, Room
from gameobjects.player import Player
from gameobjects.enemies.enemy import Enemy
from gameobjects.roomExit import RoomExit
from gamestates.gameState import GameState
from utils.helpers.surface_helper import tint_surface
from utils.ogmo.ogmoHelper import OgmoHelper

class ActionState(GameState):

    EXIT_SIZE = 96

    def enter(self):
        print("Entered Action State")

        #############################
        # SURFACES
        #############################
        self.TilesetSurface = pygame.image.load('assets/sprites/environment/tileset.png').convert_alpha()
        self.BulletSurface = pygame.image.load('assets/sprites/bullet.png').convert_alpha()
        self.EnemySurface = pygame.image.load('assets/sprites/enemies/enemy_1.png').convert_alpha()
        self.antennaSurface = pygame.image.load('assets/sprites/objects/antenna.png').convert_alpha()


        #############################
        # ENTITIES
        #############################
        p1_surf = tint_surface(pygame.image.load('assets/sprites/player/player_1.png').convert_alpha(), (23,45,34))
        self.Players = [Player(p1_surf, 100, 100, (23,45,34))]

        #############################
        # UI
        #############################
        self.UIFont = pygame.font.SysFont(None, 24)
        self.player2PressStartText = BlinkingText('Player 2 - press start', (self.game.screen.get_width() - 200, 16))


        #############################
        # Load the full, procedural Level
        #############################
        self.Level = Level()
        self.LoadRoom(self.Level.Rooms[0])


    def LoadRoom(self, room: Room | None):

        if room == None:
            return

        for player in self.Players:
            player.Bullets = []

        self.CurrentRoom = room


        #############################
        # Load a bunch of enemies
        #############################
        self.NumberOfEnemiesToSpawn = 3
        self.NumberOfEnemiesSpawned = 0 if not room.Cleared else self.NumberOfEnemiesToSpawn

        self.enemySpawningTimer = 0
        self.enemySpawnDelay = 3 # seconds
        self.Enemies = []

        #############################
        # Create the exits
        #############################
        exitLeft = RoomExit(pygame.Rect(0,0, ActionState.EXIT_SIZE, self.game.screen.get_height()), 'L')
        exitRight = RoomExit(pygame.Rect(self.game.screen.get_width() - ActionState.EXIT_SIZE, 0, ActionState.EXIT_SIZE, self.game.screen.get_height()), 'R')
        exitUp = RoomExit(pygame.Rect(0,0, self.game.screen.get_width(), ActionState.EXIT_SIZE), 'U')
        exitDown = RoomExit(pygame.Rect(0,self.game.screen.get_height() - ActionState.EXIT_SIZE, self.game.screen.get_width(), ActionState.EXIT_SIZE), 'D')
        self.Exits = []

        match self.CurrentRoom.Map.name:
            case '4ways':
                self.Exits = [exitLeft, exitRight, exitUp, exitDown]
            case '2waysLR':
                self.Exits = [exitLeft, exitRight, ]
            case '2waysUD':
                self.Exits = [exitUp, exitDown]
            case '1wayL':
                self.Exits = [exitLeft]
            case '1wayR':
                self.Exits = [exitRight]
            case '1wayU':
                self.Exits = [exitUp]
            case '1wayD':
                self.Exits = [exitDown]
        pass


    def exit(self):
        pass

    def handle_events(self, events):

        # instant presses
        for event in events:

            # KEYBOARD
            if event.type == pygame.KEYDOWN:
                if event.key == K_a: # SHOOT LEFT
                    player = self.Players[0]
                    self.Players[0].TryShootBullet(Bullet(self.BulletSurface, player.Rect.midleft, -1, 0))
                elif event.key == K_d: # SHOOT RIGHT 
                    player = self.Players[0]
                    self.Players[0].TryShootBullet(Bullet(self.BulletSurface, player.Rect.midright, 1, 0))
                elif event.key == K_w: # SHOOT UP
                    player = self.Players[0]
                    self.Players[0].TryShootBullet(Bullet(self.BulletSurface, player.Rect.midtop, 0, -1))
                elif event.key == K_s: # SHOOT DOWN
                    player = self.Players[0]
                    self.Players[0].TryShootBullet(Bullet(self.BulletSurface, player.Rect.midbottom, 0, 1))


            # JOYSTICKS
            if event.type == pygame.JOYBUTTONUP:

                # player2 joining by pressing start, spawns at p1 pos
                if event.button == 7 and event.joy == 1:
                    if len(self.Players) == 1:
                        p2_surf = tint_surface(pygame.image.load('assets/sprites/player/player_1.png').convert_alpha(), (210,120,72))
                        self.Players.append(Player(p2_surf, self.Players[0].Rect.x, self.Players[0].Rect.y, (210,120,72)))
                        self.NumberOfEnemiesToSpawn *= 3

                # only trigger input if the number of players is sufficient
                if event.joy == 0 or (event.joy == 1 and len(self.Players) == 2):
                    
                    if event.button == 2: # SHOOT LEFT
                        player = self.Players[event.joy]
                        player.TryShootBullet(Bullet(self.BulletSurface, player.Rect.midleft, -1, 0))

                    elif event.button == 1: # SHOOT RIGHT
                        player = self.Players[event.joy]
                        player.TryShootBullet(Bullet(self.BulletSurface, player.Rect.midright, 1, 0))

                    elif event.button == 3: # SHOOT UP
                        player = self.Players[event.joy]
                        player.TryShootBullet(Bullet(self.BulletSurface, player.Rect.midtop, 0, -1))

                    elif event.button == 0: # SHOOT DOWN
                        player = self.Players[event.joy]
                        player.TryShootBullet(Bullet(self.BulletSurface, player.Rect.midbottom, 0, 1))


        ######################################
        # CONTINUOUS INPUT (MOVEMENT)
        ######################################

        # KEYBOARD
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]: #or keys[K_a]:
            self.Players[0].MoveLeft(self.CurrentRoom.Obstacles)
        elif keys[K_RIGHT]: #or keys[K_d]:
            self.Players[0].MoveRight(self.CurrentRoom.Obstacles)
        if keys[K_UP]: #or keys[K_w]:
            self.Players[0].MoveUp(self.CurrentRoom.Obstacles)
        elif keys[K_DOWN]: #or keys[K_s]:
            self.Players[0].MoveDown(self.CurrentRoom.Obstacles)

        # GAMEPADS 
        for index, player in enumerate(self.Players):

            if len(self.game.joysticks) > index:

                joy = self.game.joysticks[index]

                axis_x_val = joy.get_axis(0)
                axis_y_val = joy.get_axis(1)


                # Dead zone" to prevent jitter and drift
                dead_zone_threshold = 0.1

                if abs(axis_x_val) > dead_zone_threshold:
                    player.MoveX(axis_x_val, self.CurrentRoom.Obstacles)

                if abs(axis_y_val) > dead_zone_threshold:
                    player.MoveY(axis_y_val, self.CurrentRoom.Obstacles)

                if joy.get_hat(0)[0] != 0:
                    player.MoveX(joy.get_hat(0)[0], self.CurrentRoom.Obstacles)

                if joy.get_hat(0)[1] != 0:
                    player.MoveY(joy.get_hat(0)[1] * -1, self.CurrentRoom.Obstacles)


    def update(self, dt: float):

        # blinking text
        if len(self.Players) == 1:
            self.player2PressStartText.update(dt)

        # Update players
        for player in self.Players:
            player.update(dt)

            # bound player to screen
            if player.Rect.x < 0:
                player.Rect.x = 0
            elif player.Rect.x > self.game.screen.get_width() - player.Rect.width:
                player.Rect.x = self.game.screen.get_width() - player.Rect.width

            if player.Rect.y < 0:
                player.Rect.y = 0
            elif player.Rect.y > self.game.screen.get_height() - player.Rect.height:
                player.Rect.y = self.game.screen.get_height() - player.Rect.height
            
            # check for teleport
            if self.NumberOfEnemiesSpawned >= self.NumberOfEnemiesToSpawn and len(self.Enemies) == 0:

                # that room is cleared
                self.CurrentRoom.Cleared = True

                for exit in self.Exits:
                    if player.Rect.colliderect(exit.Rect):
                        match exit.Direction:
                            case 'L':
                                self.LoadRoom(self.CurrentRoom.RoomLeft)
                                for player in self.Players:
                                    player.Rect.center = (
                                        self.game.screen.get_width() - ActionState.EXIT_SIZE * 1.5, 
                                        self.game.screen.get_height() * 0.5
                                    )
                            case 'R':
                                self.LoadRoom(self.CurrentRoom.RoomRight)
                                player.Rect.center = (
                                    int(ActionState.EXIT_SIZE * 1.5), 
                                    self.game.screen.get_height() * 0.5
                                )
                            case 'U':
                                self.LoadRoom(self.CurrentRoom.RoomUp)
                                player.Rect.center = (
                                    self.game.screen.get_width() * 0.5,
                                    self.game.screen.get_height() - ActionState.EXIT_SIZE * 1.5
                                )
                            case 'D':
                                self.LoadRoom(self.CurrentRoom.RoomDown)
                                player.Rect.center = (
                                    self.game.screen.get_width() * 0.5,
                                    int(ActionState.EXIT_SIZE * 1.5)
                                )
        # Update enemies
        for enemy in self.Enemies:
            enemy.update(self.Players, dt)

        # Update bullets
        for player in self.Players:
            for bullet in player.Bullets.copy():
                bullet.update(self.Enemies, dt)
                if bullet.lifespan >= bullet.max_lifespan:
                    player.Bullets.remove(bullet)

        # Spawn enemies
        if self.NumberOfEnemiesSpawned < self.NumberOfEnemiesToSpawn:
            self.enemySpawningTimer += dt
            if self.enemySpawningTimer >= self.enemySpawnDelay:
                self.enemySpawningTimer %= self.enemySpawnDelay

                for i in range(4 * len(self.Players)):

                    exit  = random.choice(self.Exits)
                    x = random.randrange(int(exit.Rect.centerx * 0.9), int(exit.Rect.centerx * 1.1))
                    y = random.randrange(int(exit.Rect.centery * 0.9), int(exit.Rect.centery * 1.1))

                    # x = 0
                    # y = 0
                    # rng = random.randint(1, 4)
                    # match(rng):
                    #     case 1: # TOP OF SCREEN
                    #         x = random.randrange(int(self.game.screen.get_width() * 0.25), int(self.game.screen.get_width() * 0.75))
                    #         y = -self.EnemySurface.get_height()
                    #     case 2: # BOTTOM OF SCREEN
                    #         x = random.randrange(int(self.game.screen.get_width() * 0.25), int(self.game.screen.get_width() * 0.75))
                    #         y = self.game.screen.get_height() + self.EnemySurface.get_height() 
                    #     case 3: # LEFT OF SCREEN
                    #         x = -self.EnemySurface.get_width()
                    #         y = random.randrange(int(self.game.screen.get_height() * 0.25), int(self.game.screen.get_height() * 0.75))
                    #     case 4: # RIGHT OF SCREEN
                    #         x = self.game.screen.get_width() + self.EnemySurface.get_width()
                    #         y = random.randrange(int(self.game.screen.get_height() * 0.25), int(self.game.screen.get_height() * 0.75))

                    self.Enemies.append(
                        Enemy(
                            self.EnemySurface, 
                            x,
                            y,
                            [SeekNearestPlayerBehavior(), AttackPlayerInRadiusBehavior()]
                        )
                    )
                    self.NumberOfEnemiesSpawned += 1

        # check for game over
        continueGame = any(p.Life > 0 for p in self.Players)
        if not continueGame:
            self.game.change_state("GameOver")

    def draw(self, screen):
        screen.fill((64, 64, 64))

        #############################################
        # OGMO LAYERS
        #############################################
        layers = [self.CurrentRoom.Map.layers['floor'], self.CurrentRoom.Map.layers['walls']]
        for layer in layers:
            # x_to_draw_to = 0
            y_to_draw_to = 0
            for y in range(layer.gridCellsY):
                x_to_draw_to = 0
                for x in range(layer.gridCellsX):
                    index = y * layer.gridCellsX + x # inverse: x_in_tileset, y_in_tileset = divmod(index, layer.gridCellX)
                    data = layer.data[index]

                    if data != -1:
                        # convert data in x, y in tileset
                        x_in_tileset = data * layer.gridCellWidth
                        y_in_tileset = 0

                        screen.blit(
                            self.TilesetSurface, 
                            (x_to_draw_to, y_to_draw_to), 
                            area=pygame.Rect(x_in_tileset, y_in_tileset, layer.gridCellWidth, layer.gridCellHeight)
                        )

                    x_to_draw_to += layer.gridCellWidth

                y_to_draw_to += layer.gridCellHeight

        #############################################
        # GAME OBJECTS
        #############################################
        for p in self.Players:
            p.draw(screen)

        for e in self.Enemies:
            e.draw(screen)

        for player in self.Players:
            for bullet in player.Bullets:
                bullet.draw(screen)

        #############################################
        # HUD
        #############################################
        player1ScoreText = self.UIFont.render(f'Player 1 - {self.Players[0].Score}', False, (255,255, 255))
        screen.blit(player1ScoreText, (16, 16))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(16, 32, self.Players[0].MaxLife * 20 + 6, 24))
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(19, 35, self.Players[0].Life * 20, 18))

        if len(self.Players) == 1:
            self.player2PressStartText.draw(screen)
        else:
            player2ScoreText = self.UIFont.render(f'Player 2 - {self.Players[0].Score}', False, (255, 255, 255))
            screen.blit(player2ScoreText, (self.game.screen.get_width() - 200, 16))


        # # TELEPORTS
        # if self.NumberOfEnemiesSpawned >= self.NumberOfEnemiesToSpawn and len(self.Enemies) == 0:
        #     for exit in self.Exits:
        #         pygame.draw.rect(screen, (255,0,0), exit.Rect)


    