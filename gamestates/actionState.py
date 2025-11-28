
import random
from typing import List
import pygame

from gameobjects.blinking_text import BlinkingText
from gameobjects.enemies.enemy_factory import EnemyFactory
from gameobjects.level import Level, Room
from gameobjects.objects.helpButton import HelpButton
from gameobjects.objects.objects_factory import ObjectsFactory
from gameobjects.objects.vendingmachine import VendingMachine
from gameobjects.player import Player
from gameobjects.enemies.enemy import Enemy
from gameobjects.elevator import Elevator
from gameobjects.roomExit import RoomExit
from gamestates.gameState import GameState
from utils.parameters import LOOT_CHANCE, POPUP_TEXTS, WINDOW_HEIGHT, WINDOW_WIDTH

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

        self.FloorRect = pygame.Rect(0,0, WINDOW_WIDTH, WINDOW_HEIGHT)

        #############################
        # ENTITIES
        #############################
        if self.game.players == []:
            self.game.players = [Player(1, int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))]
        self.Players = self.game.players
        self.CommTower: Enemy | None = None
        self.Elevator: Elevator | None = None
        self.FarawayTowers: List[Enemy] = []
        self.HelpButton: HelpButton | None = None
        self.VendingMachine: VendingMachine | None = None

        #############################
        # UI
        #############################
        self.UIFont = pygame.font.SysFont(None, 48)
        self.player2PressStartText = BlinkingText('Player 2 - press start', (WINDOW_WIDTH - 400, 16), font_size=48)

        self.Player1DeadText = BlinkingText('Player 1 - press start or space', (20, WINDOW_HEIGHT - 48), font_size=48)
        self.Player2DeadText = BlinkingText('Player 2 - press start or space', (WINDOW_WIDTH - 400, WINDOW_HEIGHT - 48), font_size=48)

        self.PopUpText = ''

        #############################
        # Load the full level
        #############################
        self.Level = Level(f"F{self.game.game_data['floor']}")
        self.LoadRoom(self.Level.StartingRoom)

    def LoadRoom(self, room: Room | None):

        if room == None:
            return

        self.TotalBosslife = 0
        self.Enemies = []
        self.Objects = []
        self.HelpButton = None
        self.VendingMachine = None

        for player in self.Players:
            player.Weapon.Bullets = []

        self.CurrentRoom = room
        self.RoomSurface = pygame.image.load(f'assets/sprites/environment/rooms/{room.Map.name}.png').convert_alpha()


        #############################
        # Add an help button when there is one in the room
        #############################
        if room.helpButtonDefinition is not None:
            pos = (room.helpButtonDefinition.coords[0] * WINDOW_WIDTH, room.helpButtonDefinition.coords[1] * WINDOW_HEIGHT)
            self.HelpButton = ObjectsFactory.GetHelpButton(pos, room.helpButtonDefinition.name)

        #############################
        # Add a vending machine when there is one in the room
        #############################
        if room.vendingMachineDefinition is not None:
            pos = (900,20)
            self.VendingMachine = ObjectsFactory.GetVendingMachine(pos)
            self.CurrentRoom.Obstacles.append(self.VendingMachine.Rect)


        #############################
        # Load room enemies if room not cleared
        #############################
        if not self.CurrentRoom.Cleared:
            for ed in room.EnemiesDefinitions:

                pos = (ed.coords[0] * WINDOW_WIDTH, ed.coords[1] * WINDOW_HEIGHT)
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
                        enemy = EnemyFactory.GetBombDropperEnemy(pos, self.CurrentRoom.Obstacles, self.Objects)

                    case 'miceSummoner':
                        enemy = EnemyFactory.GetMiceSummonerEnemy(pos, self.CurrentRoom.Obstacles, self.Enemies)

                    case 'default':
                        enemy = EnemyFactory.GetDefaultEnemy(pos)

                    case 'moneyDropper':
                        enemy = EnemyFactory.GetMoneyDropperEnemy(pos, self.CurrentRoom.Obstacles, self.Objects)

                    case 'turretPlus':
                        enemy = EnemyFactory.GetPlusTurret(pos)

                    case 'boss1':
                        enemy = EnemyFactory.GetBoss1(pos, self.CurrentRoom.Obstacles, self.Objects)

                    case 'boss2':
                        enemy = EnemyFactory.GetBoss2(pos, self.Objects, self.Enemies)

                    case 'boss3':
                        enemy = EnemyFactory.GetBoss3(pos, self.CurrentRoom.Obstacles, self.Objects, self.Enemies)

                if enemy is not None:
                    self.Enemies.append(enemy)
        
        # BOSS life bar
        self.TotalBosslife = sum(boss.MaxLife for boss in self.Enemies if boss.IsABoss)

        #############################
        # Add a Comm Tower here if there's one
        #############################
        if self.CurrentRoom.Coords in self.Level.CommTowerPositions:
            posX = WINDOW_WIDTH * 0.5 - self.AntennaSurface.get_width() * 0.5
            posY = WINDOW_HEIGHT * 0.5 - self.AntennaSurface.get_height() * 0.5
            self.CommTower = EnemyFactory.GetSameRoomAntennaTower((int(posX), int(posY)))
            self.Enemies.append(self.CommTower)
            self.CurrentRoom.Obstacles.append(self.CommTower.Rect)
        else:
            self.CommTower = None

        #############################
        # Add the elevator if it's here
        #############################
        if self.CurrentRoom.Coords == self.Level.ElevatorCoords:
            posX = int(WINDOW_WIDTH * 0.5 - self.ElevatorSurface.get_width() * 0.5)
            posY = int(self.ElevatorSurface.get_height() * 0.5)
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
                posX = WINDOW_WIDTH
                posXName = 'right'
            else:
                posX = WINDOW_WIDTH * .5 - self.BulletSurface.get_width() * .5
                posXName = 'mid'

            posY = 0
            posYName = ''
            if comTowerpos[1] < self.CurrentRoom.Coords[1]:
                posY = -self.BulletSurface.get_height()
                posYName = 'top'
            elif comTowerpos[1] > self.CurrentRoom.Coords[1]:
                posY = WINDOW_HEIGHT
                posYName = 'bottom'
            else:
                posY = WINDOW_HEIGHT * .5 - self.BulletSurface.get_height() * .5               
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

            tower = EnemyFactory.GetDistantAntennaTower((int(posX), int(posY)), angleRange)
            self.FarawayTowers.append(tower)

        #############################
        # Create the exits
        #############################
        exitLeft = RoomExit(pygame.Rect(0,0, ActionState.EXIT_SIZE, WINDOW_HEIGHT), 'L')
        exitRight = RoomExit(pygame.Rect(WINDOW_WIDTH - ActionState.EXIT_SIZE, 0, ActionState.EXIT_SIZE, WINDOW_HEIGHT), 'R')
        exitUp = RoomExit(pygame.Rect(0,0, WINDOW_WIDTH, ActionState.EXIT_SIZE), 'U')
        exitDown = RoomExit(pygame.Rect(0,WINDOW_HEIGHT - ActionState.EXIT_SIZE, WINDOW_WIDTH, ActionState.EXIT_SIZE), 'D')
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

        # special case for very forst room: write basic instructions on the floor
        if self.CurrentRoom == self.Level.StartingRoom and self.game.game_data['floor'] == 1:
            self.howToMoveTipSurface = pygame.image.load(f'assets/sprites/environment/rooms/moveInstructions.png').convert_alpha()


    def exit(self):
        pass

    def handle_events(self, events):

        # instant presses
        for event in events:

            # KEYBOARD
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: # SHOOT LEFT
                    player = self.Players[0]
                    self.Players[0].TryShootBullet('l')
                elif event.key == pygame.K_d: # SHOOT RIGHT 
                    player = self.Players[0]
                    self.Players[0].TryShootBullet('r')
                elif event.key == pygame.K_w: # SHOOT UP
                    player = self.Players[0]
                    self.Players[0].TryShootBullet('u')
                elif event.key == pygame.K_s: # SHOOT DOWN
                    player = self.Players[0]
                    self.Players[0].TryShootBullet('d')

                # SPACE, when P1 is dead
                elif event.key == pygame.K_SPACE:
                    self.tryRespawnPlayer(self.Players[0])

            # JOYSTICKS
            if event.type == pygame.JOYBUTTONUP:

                # player2 joining by pressing start, spawns at p1 pos
                if event.button == 7 and event.joy == 1:
                    if len(self.Players) == 1:
                        self.Players.append(Player(2, self.Players[0].Rect.x, self.Players[0].Rect.y))
                        self.NumberOfEnemiesToSpawn *= 3

                # only trigger input if the number of players is sufficient
                if event.joy == 0 or (event.joy == 1 and len(self.Players) == 2):
                    
                    if event.button == 2: # SHOOT LEFT
                        player = self.Players[event.joy]
                        player.TryShootBullet('l')

                    elif event.button == 1: # SHOOT RIGHT
                        player = self.Players[event.joy]
                        player.TryShootBullet('r')

                    elif event.button == 3: # SHOOT UP
                        player = self.Players[event.joy]
                        player.TryShootBullet('u')

                    elif event.button == 0: # SHOOT DOWN
                        player = self.Players[event.joy]
                        player.TryShootBullet('d')

                    # START BUTTON, try respawning player 
                    elif event.button == 7: 
                        self.tryRespawnPlayer(self.Players[event.joy])


        ######################################
        # CONTINUOUS INPUT (MOVEMENT)
        ######################################

        # KEYBOARD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: #or keys[K_a]:
            self.Players[0].MoveLeft(self.CurrentRoom.Obstacles)
        elif keys[pygame.K_RIGHT]: #or keys[K_d]:
            self.Players[0].MoveRight(self.CurrentRoom.Obstacles)
        if keys[pygame.K_UP]: #or keys[K_w]:
            self.Players[0].MoveUp(self.CurrentRoom.Obstacles)
        elif keys[pygame.K_DOWN]: #or keys[K_s]:
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
        if self.Players[0].CurrentLife <= 0:
            text = 'Player 1 - press start or space' if self.Players[0].Lives > 0 else 'Player 1 - GAME OVER'
            self.Player1DeadText.renderNewText(text)
            self.Player1DeadText.update(dt)

        if len(self.Players) == 1:
            self.player2PressStartText.update(dt)
        elif self.Players[1].CurrentLife <= 0:
            text = 'Player 2 - press start or space' if self.Players[1].Lives > 0 else 'Player 2 - GAME OVER'
            self.Player2DeadText.renderNewText(text)
            self.Player2DeadText.update(dt)

        # Update players
        for player in self.Players:
            player.update(self.Enemies, dt)

            # bound player to screen
            if player.Rect.x < 0:
                player.Rect.x = 0
            elif player.Rect.x > WINDOW_WIDTH - player.Rect.width:
                player.Rect.x = WINDOW_WIDTH - player.Rect.width

            if player.Rect.y < 0:
                player.Rect.y = 0
            elif player.Rect.y > WINDOW_HEIGHT - player.Rect.height:
                player.Rect.y = WINDOW_HEIGHT - player.Rect.height
            
            # check for items pickups
            for object in self.Objects.copy():
                if player.Rect.colliderect(object.Rect):
                    object.handleCollision(player)
                    if object.canBePickedUp:
                        self.Objects.remove(object)
                    
            # check for collision with help button
            if self.HelpButton is not None and player.Rect.colliderect(self.HelpButton.Rect) and len(self.Enemies) == 0:
                self.PopUpText = self.HelpButton.textKey
            else:
                self.PopUpText = ''

            if self.VendingMachine is not None:
                self.VendingMachine.handleCollision(player)


            # check for teleport to next floor
            if self.Elevator is not None and self.CurrentRoom.Cleared and len(self.FarawayTowers) == 0:
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
                                        WINDOW_WIDTH - ActionState.EXIT_SIZE - 1, 
                                        int(WINDOW_HEIGHT * 0.5)
                                    )
                            case 'R':
                                self.LoadRoom(self.Level.GetRoomByCoords(self.CurrentRoom.Coords[0] + 1, self.CurrentRoom.Coords[1]))
                                for player in self.Players:
                                    player.Rect.midleft = (
                                        ActionState.EXIT_SIZE + 1, 
                                        int(WINDOW_HEIGHT * 0.5)
                                    )
                            case 'U':
                                self.LoadRoom(self.Level.GetRoomByCoords(self.CurrentRoom.Coords[0], self.CurrentRoom.Coords[1] - 1))
                                for player in self.Players:
                                    player.Rect.midbottom = (
                                        int(WINDOW_WIDTH * 0.5),
                                        WINDOW_HEIGHT - ActionState.EXIT_SIZE - 1
                                    )
                            case 'D':
                                self.LoadRoom(self.Level.GetRoomByCoords(self.CurrentRoom.Coords[0], self.CurrentRoom.Coords[1] + 1))
                                for player in self.Players:
                                    player.Rect.midtop = (
                                        int(WINDOW_WIDTH * 0.5),
                                        int(ActionState.EXIT_SIZE + 1)
                                    )

        # update objects and remove them if needed
        for object in self.Objects.copy():
            object.update(dt)

            if object.lifespan >= object.maxlifespan:
                self.Objects.remove(object)

        # Update enemies
        for enemy in self.Enemies.copy():

            if not enemy.Rect.colliderect(self.FloorRect):
                self.Enemies.remove(enemy)
                break

            if enemy.CurrentLife <= 0:

                # increase the score of the player who killed the enemy
                if enemy.KilledByPlayerIndex is not None:
                    player = self.Players[enemy.KilledByPlayerIndex - 1]
                    player.Score += enemy.ScoreValue

                    # gain a life if score 
                    if player.Score > player.NextLifeThreshold:
                        player.NextLifeThreshold += 1500
                        player.Lives += 1

                # loot chance!
                
                if random.random() <= LOOT_CHANCE:
                    rng = random.random()
                    if rng < 0.5:
                        self.Objects.append(ObjectsFactory.GetMedkit(enemy.Rect.bottomleft))
                    else:
                        self.Objects.append(ObjectsFactory.GetRandomWeaponPickup(enemy.Rect.bottomleft))
                        
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
        continueGame = any(p.CurrentLife > 0 or p.Lives > 0 for p in self.Players)
        if not continueGame:
            print(self.Players[0].Lives)
            self.game.change_state("GameOver")

    def draw(self, screen):
        screen.fill((64, 64, 64))

        #############################################
        # DRAW CURRENT ROOM BY NAME
        #############################################
        screen.blit(self.RoomSurface, (0,0))

        #############################################
        # SPECIAL CASE FOR VERY FIRST ROOM: WRITE INSTRUCTIONS
        #############################################
        if self.CurrentRoom == self.Level.StartingRoom and self.game.game_data['floor'] == 1:
            screen.blit(self.howToMoveTipSurface, (WINDOW_WIDTH / 2 - self.howToMoveTipSurface.get_width() / 2, WINDOW_HEIGHT / 2- self.howToMoveTipSurface.get_height() / 2))

        #############################################
        # GAME OBJECTS
        #############################################

        if self.HelpButton is not None:
            self.HelpButton.draw(screen)

        if self.VendingMachine is not None:
            self.VendingMachine.draw(screen)


        if self.CommTower:
            self.CommTower.draw(screen)

        if self.Elevator:
            self.Elevator.draw(screen)

        for o in self.Objects:
            if o.BlinkingComponent.visible:
                o.draw(screen)

        for e in self.Enemies:
            e.draw(screen)

        for p in self.Players:
            p.draw(screen)

        for t in self.FarawayTowers:
            t.draw(screen)

        #############################################
        # ROOM BOTTOM CORNERS
        #############################################
        screen.blit(self.RoomBottomLeftCornerSurface, (0, WINDOW_HEIGHT - self.RoomBottomLeftCornerSurface.get_height()))
        screen.blit(self.RoomBottomRightCornerSurface, (WINDOW_WIDTH - self.RoomBottomRightCornerSurface.get_width(), WINDOW_HEIGHT - self.RoomBottomRightCornerSurface.get_height()))

        #############################################
        # POPUP TEXT WHEN STEPPING ON HELP BUTTONS
        #############################################
        if self.PopUpText != '':
            lines = POPUP_TEXTS[self.PopUpText]
            lineY = 600
            lineX = 200

            pygame.draw.rect(screen, (72, 55, 55), pygame.Rect(lineX - 20, lineY - 20, WINDOW_WIDTH - (lineX - 20) * 2, len(lines) * 40 + 20))

            font = pygame.font.SysFont(None, 32)
            for line in lines:
                text = font.render(line, True, (255, 255, 255))
                screen.blit(text, (lineX, lineY))
                lineY += 40

        #############################################
        # HUD
        #############################################
        
        # P1 score & life bar
        player1ScoreText = self.UIFont.render(f'Player 1 - {self.Players[0].Score} ({self.Players[0].Lives} lives)', False, (255,255, 255))
        screen.blit(player1ScoreText, (16, 16))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(16, 64, self.Players[0].MaxLife * 20 + 6, 24))
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(19, 67, self.Players[0].CurrentLife * 20, 18))

        if self.Players[0].CurrentLife <= 0:
            self.Player1DeadText.draw(screen)

        if len(self.Players) == 1:
            self.player2PressStartText.draw(screen)
        else:
            player2ScoreText = self.UIFont.render(f'Player 2 - {self.Players[1].Score} ({self.Players[1].Lives} lives)', False, (255, 255, 255))
            screen.blit(player2ScoreText, (WINDOW_WIDTH - 200, 16))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(16, 64, self.Players[1].MaxLife * 20 + 6, 24))
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(19, 67, self.Players[1].CurrentLife * 20, 18))

            if self.Players[1].CurrentLife <= 0:
                self.Player2DeadText.draw(screen)

        # Boss life bar
        if self.TotalBosslife > 0:
            self.CurrentBosslife = sum(boss.CurrentLife for boss in self.Enemies if boss.IsABoss)

            if self.CurrentBosslife > 0:
                maxWidth = WINDOW_WIDTH - 394
                currentWidth = self.CurrentBosslife / self.TotalBosslife * maxWidth - 6

                pygame.draw.rect(screen, (0,0,0), pygame.Rect(197, WINDOW_HEIGHT - 75, maxWidth, 48))
                pygame.draw.rect(screen, (255,0,0), pygame.Rect(200, WINDOW_HEIGHT - 72, currentWidth, 42))


    def tryRespawnPlayer(self, player: Player):
        if player.Lives <= 0 or player.CurrentLife > 0:
            return
        
        player.Lives -= 1
        player.CurrentLife = player.MaxLife
        player.initializeWeapon()
        player.BlinkingComponent.StartBlinking()