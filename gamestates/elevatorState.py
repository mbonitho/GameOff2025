import pygame
from pygame.locals import *

from gameobjects.blinking_text import BlinkingText
from gameobjects.player import Player
from gameobjects.room import Room
from gamestates.gameState import GameState
from utils.helpers.surface_helper import tint_surface
from utils.ogmo.ogmoHelper import OgmoHelper

class ElevatorState(GameState):

    EXIT_SIZE = 48

    def enter(self):
        print("Entered Elevator State")

        #############################
        # SURFACES
        #############################
        self.TilesetSurface = pygame.image.load('assets/sprites/environment/tileset.png').convert_alpha()


        #############################
        # ENTITIES
        #############################
        p1_surf = tint_surface(pygame.image.load('assets/sprites/player/player_1.png').convert_alpha(), (23,45,34))
        self.Players = [Player(p1_surf, 100, 100, (23,45,34))]

        #############################
        # UI
        #############################
        self.UIFont = pygame.font.SysFont(None, 48)
        self.player2PressStartText = BlinkingText('Player 2 - press start', (self.game.screen.get_width() - 400, 16), font_size=48)


        #############################
        # Load the elevator
        #############################
        # self.Level = Level(f'F{self.game.game_data['floor']}')
        # self.LoadRoom(self.Level.StartingRoom)
        self.elevatorRoom = Room(OgmoHelper.get_map('elevator', 'rooms/special_rooms'), (0,0))
        self.elevatorRoom.GenerateObstacles()

        self.XOffset = 200
        self.YOffset = 0


    def exit(self):
        pass

    def handle_events(self, events):

        # instant presses
        for event in events:

            # JOYSTICKS
            if event.type == pygame.JOYBUTTONUP:

                # player2 joining by pressing start, spawns at p1 pos
                if event.button == 7 and event.joy == 1:
                    if len(self.Players) == 1:
                        p2_surf = tint_surface(pygame.image.load('assets/sprites/player/player_1.png').convert_alpha(), (210,120,72))
                        self.Players.append(Player(p2_surf, self.Players[0].Rect.x, self.Players[0].Rect.y, (210,120,72)))


        ######################################
        # CONTINUOUS INPUT (MOVEMENT)
        ######################################

        # KEYBOARD
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]: #or keys[K_a]:
            self.Players[0].MoveLeft(self.elevatorRoom.Obstacles)
        elif keys[K_RIGHT]: #or keys[K_d]:
            self.Players[0].MoveRight(self.elevatorRoom.Obstacles)
        if keys[K_UP]: #or keys[K_w]:
            self.Players[0].MoveUp(self.elevatorRoom.Obstacles)
        elif keys[K_DOWN]: #or keys[K_s]:
            self.Players[0].MoveDown(self.elevatorRoom.Obstacles)

        elif keys[K_a]:
            self.game.change_state("Action")

        # GAMEPADS 
        for index, player in enumerate(self.Players):

            if len(self.game.joysticks) > index:

                joy = self.game.joysticks[index]

                axis_x_val = joy.get_axis(0)
                axis_y_val = joy.get_axis(1)


                # Dead zone" to prevent jitter and drift
                dead_zone_threshold = 0.1

                if abs(axis_x_val) > dead_zone_threshold:
                    player.MoveX(axis_x_val, self.elevatorRoom.Obstacles)

                if abs(axis_y_val) > dead_zone_threshold:
                    player.MoveY(axis_y_val, self.elevatorRoom.Obstacles)

                if joy.get_hat(0)[0] != 0:
                    player.MoveX(joy.get_hat(0)[0], self.elevatorRoom.Obstacles)

                if joy.get_hat(0)[1] != 0:
                    player.MoveY(joy.get_hat(0)[1] * -1, self.elevatorRoom.Obstacles)


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
            
            

    def draw(self, screen):
        screen.fill((64, 64, 64))

        #############################################
        # OGMO LAYERS
        #############################################
        layers = [self.elevatorRoom.Map.layers['floor'], self.elevatorRoom.Map.layers['walls']]
        for layer in layers:
            # x_to_draw_to = 0
            y_to_draw_to = self.YOffset
            for y in range(layer.gridCellsY):
                x_to_draw_to = self.XOffset
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
    