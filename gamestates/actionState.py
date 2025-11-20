
import random
from typing import List
import pygame
from pygame.locals import *

from gameobjects.blinking_text import BlinkingText
from gameobjects.bullet import Bullet
from gameobjects.enemies.enemy_factory import EnemyFactory
from gameobjects.level import Level, Room
from gameobjects.objects.objects_factory import ObjectsFactory
from gameobjects.player import Player
from gameobjects.enemies.enemy import Enemy
from gameobjects.elevator import Elevator
from gameobjects.roomExit import RoomExit
from gamestates.gameState import GameState
from utils.parameters import MEDKIT_CHANCE

class ActionState(GameState):

    EXIT_SIZE = 48

    def enter(self):
        print("Entered Action State")

        #############################
        # SURFACES
        #############################
        self.TilesetSurface = pygame.image.load('assets/sprites/environment/tileset.png').convert_alpha()
        self.BulletSurface = pygame.image.load('assets/sprites/projectiles/bullet.png').convert_alpha()
        self.AntennaSurface = pygame.image.load('assets/sprites/objects/antenna.png').convert_alpha()
        self.ElevatorSurface = pygame.image.load('assets/sprites/objects/elevator_1.png').convert_alpha()
        self.RoomSurface: pygame.Surface 

        self.RoomBottomLeftCornerSurface = pygame.image.load('assets/sprites/environment/rooms/roomBottomLeftCorner.png').convert_alpha()
        self.RoomBottomRightCornerSurface = pygame.image.load('assets/sprites/environment/rooms/roomBottomRightCorner.png').convert_alpha()


        #############################
        # ENTITIES
        #############################
        self.Players = [Player(1, self.game.GAME_WINDOW_SIZE[0] / 2, self.game.GAME_WINDOW_SIZE[1] / 2)]
        self.CommTower: Enemy | None = None
        self.Elevator: Elevator | None = None
        self.FarawayTowers: List[Enemy] = []


        #############################
        # UI
        #############################
        self.UIFont = pygame.font.SysFont(None, 48)
        self.player2PressStartText = BlinkingText('Player 2 - press start', (self.game.GAME_WINDOW_SIZE[0] - 400, 16), font_size=48)


        #############################
        # Load the full level
        #############################
        # self.NumberOfEnemiesToSpawn = 0
        # self.NumberOfEnemiesSpawned = 0
        self.Level = Level(f'F{self.game.game_data['floor']}')
        self.LoadRoom(self.Level.StartingRoom)

    def LoadRoom(self, room: Room | None):

        if room == None:
            return

        self.Enemies = []
        self.Objects = []

        for player in self.Players:
            player.Bullets = []

        self.CurrentRoom = room
        self.RoomSurface = pygame.image.load(f'assets/sprites/environment/rooms/{room.Map.name}.png').convert_alpha()

        #############################
        # Load room enemies if room not cleared
        #############################
        if not self.CurrentRoom.Cleared:
            for ed in room.EnemiesDefinitions:

                pos = (ed.Coords[0] * self.game.GAME_WINDOW_SIZE[0], ed.Coords[1] * self.game.GAME_WINDOW_SIZE[1])
                enemy = None
                match ed.name:
                    case 'smallFast':
                        enemy = EnemyFactory.GetSmallFastEnemy(pos)

                    case 'patrollingH':
                        enemy = EnemyFactory.GetPatrollingEnemy(pos, self.CurrentRoom.Obstacles, 'h')

                    case 'patrollingV':
                        enemy = EnemyFactory.GetPatrollingEnemy(pos, self.CurrentRoom.Obstacles, 'v')

                    case 'mineDropper':
                        enemy = EnemyFactory.GetMineDropperEnemy(pos, self.CurrentRoom.Obstacles, self.Objects)

                    case 'bigSlow':
                        enemy = EnemyFactory.GetBigSlowEnemy(pos)

                    case 'bombDropper':
                        enemy = EnemyFactory.GetBombDropperEnemy(pos)

                    case 'miceSummoner':
                        enemy = EnemyFactory.GetMiceSummonerEnemy(pos)

                    case 'default':
                        enemy = EnemyFactory.GetDefaultEnemy(pos)

                    case 'moneyDropper':
                        enemy = EnemyFactory.GetMoneyDropperEnemy(pos, self.CurrentRoom.Obstacles, self.Objects)

                    case 'turretPlus':
                        enemy = EnemyFactory.GetPlusTurret(pos)

                if enemy is not None:
                    self.Enemies.append(enemy)

        #############################
        # Add a Comm Tower here if there's one
        #############################
        if self.CurrentRoom.Coords in self.Level.CommTowerPositions:
            posX = self.game.screen.get_width() * 0.5 - self.AntennaSurface.get_width() * 0.5
            posY = self.game.screen.get_height() * 0.5 - self.AntennaSurface.get_height() * 0.5
            self.CommTower = EnemyFactory.GetSameRoomAntennaTower((posX, posY))
            self.Enemies.append(self.CommTower)
            self.CurrentRoom.Obstacles.append(self.CommTower.Rect)
        else:
            self.CommTower = None

        #############################
        # Add the elevator if it's here
        #############################
        if self.CurrentRoom.Coords == self.Level.ElevatorCoords:
            posX = self.game.screen.get_width() * 0.5 - self.ElevatorSurface.get_width() * 0.5
            posY = self.ElevatorSurface.get_height() * 0.5
            self.Elevator = Elevator(self.ElevatorSurface, posX, posY)
            # self.CurrentRoom.Obstacles.append(self.Elevator.Rect)
        else:
            self.Elevator = None

        #############################
        # Initialize the faraway towers
        #############################
        self.FarawayTowers: List[Enemy] = []
        for comTowerpos in self.Level.CommTowerPositions:

            if comTowerpos == self.CurrentRoom.Coords:
                continue # ignore current room

            posX = 0
            posXName = ''
            if comTowerpos[0] < self.CurrentRoom.Coords[0]:
                posX = -self.BulletSurface.get_width()
                posXName = 'left'
            elif comTowerpos[0] > self.CurrentRoom.Coords[0]:
                posX = self.game.screen.get_width()
                posXName = 'right'
            else:
                posX = self.game.screen.get_width() * .5 - self.BulletSurface.get_width() * .5
                posXName = 'mid'

            posY = 0
            posYName = ''
            if comTowerpos[1] < self.CurrentRoom.Coords[1]:
                posY = -self.BulletSurface.get_height()
                posYName = 'top'
            elif comTowerpos[1] > self.CurrentRoom.Coords[1]:
                posY = self.game.screen.get_height()
                posYName = 'bottom'
            else:
                posY = self.game.screen.get_height() * .5 - self.BulletSurface.get_height() * .5               
                posYName = 'mid'

            angleRange: tuple[int, int]

            # midleft
            if posXName == 'right' and posYName == 'mid':
                angleRange = (150, 210)
            # topleft
            elif posXName == 'right' and posYName == 'bottom':
                angleRange = (105, 165)
            # midtop
            elif posXName == 'mid' and posYName == 'bottom':
                angleRange = (60, 120)
            # topright
            elif posXName == 'left' and posYName == 'bottom':
                angleRange = (15, 75)
            # midright
            elif posXName == 'left' and posYName == 'mid':
                angleRange = (-30, 30)
            # bottomright
            elif posXName == 'left' and posYName == 'top':
                angleRange = (300, 360)
            # midbottom
            elif posXName == 'mid' and posYName == 'top':
                angleRange = (105, 165)
            # bottomleft
            elif posXName == 'right' and posYName == 'top':
                angleRange = (195, 255)

            tower = EnemyFactory.GetDistantAntennaTower((posX, posY), angleRange)
            self.FarawayTowers.append(tower)

        #############################
        # Create the exits
        #############################
        exitLeft = RoomExit(pygame.Rect(0,0, ActionState.EXIT_SIZE, self.game.screen.get_height()), 'L')
        exitRight = RoomExit(pygame.Rect(self.game.GAME_WINDOW_SIZE[0] - ActionState.EXIT_SIZE, 0, ActionState.EXIT_SIZE, self.game.GAME_WINDOW_SIZE[1]), 'R')
        exitUp = RoomExit(pygame.Rect(0,0, self.game.GAME_WINDOW_SIZE[0], ActionState.EXIT_SIZE), 'U')
        exitDown = RoomExit(pygame.Rect(0,self.game.GAME_WINDOW_SIZE[1] - ActionState.EXIT_SIZE, self.game.GAME_WINDOW_SIZE[0], ActionState.EXIT_SIZE), 'D')
        self.Exits = []

        match self.CurrentRoom.Map.name:
            case '4ways':
                self.Exits = [exitLeft, exitRight, exitUp, exitDown]
            case '2waysLR':
                self.Exits = [exitLeft, exitRight]
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
            case '2waysLU':
                self.Exits = [exitLeft, exitUp]
            case '2waysUR':
                self.Exits = [exitUp, exitRight]
            case '2waysRD':
                self.Exits = [exitRight, exitDown]
            case '2waysDL':
                self.Exits = [exitDown, exitLeft]
            case '3waysLUD':
                self.Exits = [exitLeft, exitUp, exitDown]
            case '3waysLUR':
                self.Exits = [exitLeft, exitUp, exitRight]
            case '3waysURD':
                self.Exits = [exitUp, exitRight, exitDown]     
            case '3waysLRD':
                self.Exits = [exitLeft, exitRight, exitDown]

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
                    self.Players[0].TryShootBullet(Bullet(self.BulletSurface, player.Rect.midleft, 180))
                elif event.key == K_d: # SHOOT RIGHT 
                    player = self.Players[0]
                    self.Players[0].TryShootBullet(Bullet(self.BulletSurface, player.Rect.midright, 0))
                elif event.key == K_w: # SHOOT UP
                    player = self.Players[0]
                    self.Players[0].TryShootBullet(Bullet(self.BulletSurface, player.Rect.midtop, 270))
                elif event.key == K_s: # SHOOT DOWN
                    player = self.Players[0]
                    self.Players[0].TryShootBullet(Bullet(self.BulletSurface, player.Rect.midbottom, 90))


            # JOYSTICKS
            if event.type == pygame.JOYBUTTONUP:

                # player2 joining by pressing start, spawns at p1 pos
                if event.button == 7 and event.joy == 1:
                    if len(self.Players) == 1:
                        self.Players.append(Player(2, self.Players[0].Rect.x, self.Players[0].Rect.y, (210,120,72)))
                        self.NumberOfEnemiesToSpawn *= 3

                # only trigger input if the number of players is sufficient
                if event.joy == 0 or (event.joy == 1 and len(self.Players) == 2):
                    
                    if event.button == 2: # SHOOT LEFT
                        player = self.Players[event.joy]
                        player.TryShootBullet(Bullet(self.BulletSurface, player.Rect.midleft, 180))

                    elif event.button == 1: # SHOOT RIGHT
                        player = self.Players[event.joy]
                        player.TryShootBullet(Bullet(self.BulletSurface, player.Rect.midright, 0))

                    elif event.button == 3: # SHOOT UP
                        player = self.Players[event.joy]
                        player.TryShootBullet(Bullet(self.BulletSurface, player.Rect.midtop, 270))

                    elif event.button == 0: # SHOOT DOWN
                        player = self.Players[event.joy]
                        player.TryShootBullet(Bullet(self.BulletSurface, player.Rect.midbottom, 90))


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
            elif player.Rect.x > self.game.GAME_WINDOW_SIZE[0] - player.Rect.width:
                player.Rect.x = self.game.GAME_WINDOW_SIZE[0] - player.Rect.width

            if player.Rect.y < 0:
                player.Rect.y = 0
            elif player.Rect.y > self.game.GAME_WINDOW_SIZE[1] - player.Rect.height:
                player.Rect.y = self.game.GAME_WINDOW_SIZE[1] - player.Rect.height
            
            # check for items pickups
            for object in self.Objects.copy():
                if player.Rect.colliderect(object.Rect) and object.canBePickedUp:
                    object.handleCollision(player)
                    self.Objects.remove(object)
                    
            # check for teleport to next floor
            if self.Elevator:
                if player.Rect.colliderect(self.Elevator.Rect):
                    self.game.game_data['floor'] += 1
                    self.game.change_state("Elevator")

            # check for teleport to adjacent room
            if len(self.Enemies) == 0:

                # that room is cleared
                self.CurrentRoom.Cleared = True

                for exit in self.Exits:
                    if player.Rect.colliderect(exit.Rect):
                        match exit.Direction:
                            case 'L':
                                self.LoadRoom(self.Level.GetRoomByCoords(x=self.CurrentRoom.Coords[0] - 1, y=self.CurrentRoom.Coords[1]))
                                for player in self.Players:
                                    player.Rect.midright = (
                                        self.game.GAME_WINDOW_SIZE[0] - ActionState.EXIT_SIZE - 1, 
                                        self.game.GAME_WINDOW_SIZE[1] * 0.5
                                    )
                            case 'R':
                                self.LoadRoom(self.Level.GetRoomByCoords(self.CurrentRoom.Coords[0] + 1, self.CurrentRoom.Coords[1]))
                                for player in self.Players:
                                    player.Rect.midleft = (
                                        ActionState.EXIT_SIZE + 1, 
                                        self.game.GAME_WINDOW_SIZE[1] * 0.5
                                    )
                            case 'U':
                                self.LoadRoom(self.Level.GetRoomByCoords(self.CurrentRoom.Coords[0], self.CurrentRoom.Coords[1] - 1))
                                for player in self.Players:
                                    player.Rect.midbottom = (
                                        self.game.GAME_WINDOW_SIZE[0] * 0.5,
                                        self.game.GAME_WINDOW_SIZE[1] - ActionState.EXIT_SIZE - 1
                                    )
                            case 'D':
                                self.LoadRoom(self.Level.GetRoomByCoords(self.CurrentRoom.Coords[0], self.CurrentRoom.Coords[1] + 1))
                                for player in self.Players:
                                    player.Rect.midtop = (
                                        self.game.GAME_WINDOW_SIZE[0] * 0.5,
                                        int(ActionState.EXIT_SIZE + 1)
                                    )

        # Update bullets
        for index, player in enumerate(self.Players):
            for bullet in player.Bullets.copy():
                bullet.update(self.Enemies, dt, index)
                if bullet.lifespan >= bullet.max_lifespan:
                    player.Bullets.remove(bullet)

        # update objects and remove them if needed
        for object in self.Objects.copy():
            object.update(dt)

            if object.lifespan >= object.maxlifespan:
                self.Objects.remove(object)

        # Update enemies
        for enemy in self.Enemies.copy():
            if enemy.CurrentLife <= 0:

                # increase the score of the player who killed the enemy
                if enemy.KilledByPlayerIndex:
                    player = self.Players[enemy.KilledByPlayerIndex]
                    player.Score += enemy.ScoreValue

                # loot chance!
                rng = random.random()
                if rng <= MEDKIT_CHANCE:
                    self.Objects.append(ObjectsFactory.GetMedkit(enemy.Rect.bottomleft))

                self.Enemies.remove(enemy)

            enemy.update(self.Players, dt)



        # Comm towers shoot waves from other rooms
        for tower in self.FarawayTowers:
            tower.update(self.Players, dt)

        # Check if comm tower is destroyed
        if self.CommTower and self.CommTower.CurrentLife <= 0:
            self.CurrentRoom.Obstacles.remove(self.CommTower.Rect)
            self.Level.CommTowerPositions.remove(self.CurrentRoom.Coords)
            self.CommTower = None

        # check for game over
        continueGame = any(p.CurrentLife > 0 for p in self.Players)
        if not continueGame:
            self.game.change_state("GameOver")

    def draw(self, screen):
        screen.fill((64, 64, 64))

        #############################################
        # OGMO LAYERS (not used anymore)
        #############################################
        # layers = [self.CurrentRoom.Map.layers['floor'], self.CurrentRoom.Map.layers['walls']]
        # for layer in layers:
        #     # x_to_draw_to = 0
        #     y_to_draw_to = 0
        #     for y in range(layer.gridCellsY):
        #         x_to_draw_to = 0
        #         for x in range(layer.gridCellsX):
        #             index = y * layer.gridCellsX + x # inverse: x_in_tileset, y_in_tileset = divmod(index, layer.gridCellX)
        #             data = layer.data[index]

        #             if data != -1:
        #                 # convert data in x, y in tileset
        #                 x_in_tileset = data * layer.gridCellWidth
        #                 y_in_tileset = 0

        #                 screen.blit(
        #                     self.TilesetSurface, 
        #                     (x_to_draw_to, y_to_draw_to), 
        #                     area=pygame.Rect(x_in_tileset, y_in_tileset, layer.gridCellWidth, layer.gridCellHeight)
        #                 )

        #             x_to_draw_to += layer.gridCellWidth

        #         y_to_draw_to += layer.gridCellHeight


        #############################################
        # DRAW CURRENT ROOM BY NAME
        #############################################
        screen.blit(self.RoomSurface, (0,0))

        #############################################
        # SPECIAL CASE FOR VERY FIRST ROOM: WRITE INSTRUCTIONS
        #############################################
        if self.CurrentRoom == self.Level.StartingRoom and self.game.game_data['floor'] == 1:

            lines = [
                "Welcome to Project W.A.V.E.S!",
                "",
                "Use arrow keys to move and W/A/S/D to shoot up/left/down/right",
                "",
                "Or use a gamepad (d-pad or left stick to move, A/B/X/Y to shoot)",
                "",
                "If your keyboard isn't qwerty or your gamepad buttons are scrambled, fear not!",
                "Just press the Ctrl key to configure your keyboard or gamepad."
            ]
            font = pygame.font.SysFont(None, 32)
            lineY = 200
            for line in lines:
                text = font.render(line, True, (255, 255, 255))
                screen.blit(text, (200, lineY))
                lineY += 40


        #############################################
        # GAME OBJECTS
        #############################################

        for e in self.Enemies:
            e.draw(screen)

        if self.CommTower:
            self.CommTower.draw(screen)

        if self.Elevator:
            self.Elevator.draw(screen)

        for o in self.Objects:
            if o.BlinkingComponent.visible:
                o.draw(screen)

        for p in self.Players:
            p.draw(screen)

        for t in self.FarawayTowers:
            t.draw(screen)

        for player in self.Players:
            for bullet in player.Bullets:
                bullet.draw(screen)


        #############################################
        # ROOM BOTTOM CORNERS
        #############################################
        screen.blit(self.RoomBottomLeftCornerSurface, (0,self.game.screen.get_height() - self.RoomBottomLeftCornerSurface.get_height()))
        screen.blit(self.RoomBottomRightCornerSurface, (self.game.screen.get_width() - self.RoomBottomRightCornerSurface.get_width(), self.game.screen.get_height() - self.RoomBottomRightCornerSurface.get_height()))


        #############################################
        # HUD
        #############################################
        player1ScoreText = self.UIFont.render(f'Player 1 - {self.Players[0].Score}', False, (255,255, 255))
        screen.blit(player1ScoreText, (16, 16))

        # P1 life bar
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(16, 64, self.Players[0].MaxLife * 20 + 6, 24))
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(19, 67, self.Players[0].CurrentLife * 20, 18))

        if len(self.Players) == 1:
            self.player2PressStartText.draw(screen)
        else:
            player2ScoreText = self.UIFont.render(f'Player 2 - {self.Players[0].Score}', False, (255, 255, 255))
            screen.blit(player2ScoreText, (self.game.screen.get_width() - 200, 16))
    