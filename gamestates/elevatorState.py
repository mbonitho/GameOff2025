import pygame
from pygame.locals import *

from gameobjects.blinking_text import BlinkingText
from gameobjects.player import Player
from gameobjects.room import Room
from gamestates.gameState import GameState
from utils.ogmo.ogmoMap import OgmoMap

class ElevatorState(GameState):

    EXIT_SIZE = 48

    def enter(self):
        print("Entered Elevator State")

        self.XOffset = 200
        self.YOffset = 1000
        self.scrollingSpeed = -100


        #############################
        # SURFACES
        #############################
        self.RoomSurface = pygame.image.load('assets/sprites/environment/rooms/elevatorRoom.png').convert_alpha()

        #############################
        # ENTITIES
        #############################
        self.floorRect = pygame.Rect(self.XOffset + 64, self.YOffset + 64, 300, 236)
        self.Players = [Player(1, int(self.floorRect.x + self.floorRect.width / 2), 0)]

        #############################
        # UI
        #############################
        self.UIFont = pygame.font.SysFont(None, 48)
        self.FloorFont = pygame.font.SysFont(None, 96)
        self.player2PressStartText = BlinkingText('Player 2 - press start', (self.game.screen.get_width() - 400, 16), font_size=48)
        
        self.previousFloorText = self.FloorFont.render(f"F{self.game.game_data['floor'] - 1}", False, (255,255,255))
        self.previousFloorTextPos = self.game.GAME_WINDOW_SIZE[1] / 2

        self.nextFloorText = self.FloorFont.render(f"F{self.game.game_data['floor']}", False, (255,255,255))
        self.nextFloorTextPos = self.game.GAME_WINDOW_SIZE[1] * 1.75

        #############################
        # Load the elevator
        #############################
        self.elevatorRoom = Room(OgmoMap(), (0,0))

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
                        self.Players.append(Player(2, self.Players[0].Rect.x, self.Players[0].Rect.y))

            if self.game.game_data['floor'] > 2:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        self.game.change_state("Action")

                if event.type == pygame.JOYBUTTONUP:
                    if event.button == 7 and event.joy == 0:
                        self.game.change_state("Action")

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

        # raise everything
        self.YOffset += self.scrollingSpeed * dt
        self.floorRect = pygame.Rect(self.XOffset + 64, self.YOffset + 64, 300, 236)
        self.previousFloorTextPos += self.scrollingSpeed * dt
        self.nextFloorTextPos += self.scrollingSpeed * dt

        # end of animation
        if self.YOffset <= -360:
            self.game.change_state("Action")

        # blinking text
        if len(self.Players) == 1:
            self.player2PressStartText.update(dt)

        # Update players
        for player in self.Players:
            player.update([], dt)

            # bound player to floor
            if player.Rect.x < self.floorRect.x:
                player.Rect.x = self.floorRect.x
            elif player.Rect.x > self.floorRect.right - player.Rect.width:
                player.Rect.x = self.floorRect.right - player.Rect.width

            if player.Rect.y + self.floorRect.y < self.floorRect.y:
                player.Rect.y = self.floorRect.y - self.floorRect.y
            elif player.Rect.y + self.floorRect.y > self.floorRect.bottom - player.Rect.height:
                player.Rect.y = self.floorRect.bottom - player.Rect.height - self.floorRect.y
            
            

    def draw(self, screen):
        screen.fill((64, 64, 64))

        screen.blit(self.RoomSurface, (self.XOffset, self.YOffset))

        # pygame.draw.rect(screen, (255, 0, 0), self.floorRect)

        #############################################
        # GAME OBJECTS
        #############################################
        for p in self.Players:
            img = p.animations[p.state][p.frame_index]
            if not p.looking_right:
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (p.Rect.x, p.Rect.y + self.floorRect.y))

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
    
        # Floor numbers
        screen.blit(self.previousFloorText, (700, self.previousFloorTextPos))
        screen.blit
        
        if self.game.game_data['floor'] > 2:
            font = pygame.font.SysFont(None, 24)
            text = font.render('(Press space or start to skip)', True, (255, 255, 255))
            screen.blit(text, (self.game.GAME_WINDOW_SIZE[0] / 2 - text.get_width()/ 2, 20))
