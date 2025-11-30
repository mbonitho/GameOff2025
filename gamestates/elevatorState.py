import pygame

from gameobjects.blinking_text import BlinkingText
from gameobjects.player import Player
from gameobjects.room import Room
from gamestates.gameState import GameState
from utils.ogmo.ogmoMap import OgmoMap
from utils.parameters import WINDOW_HEIGHT, WINDOW_WIDTH
from utils.sfx_factory import SFXFactory

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
        self.Players = self.game.players

        #############################
        # UI
        #############################
        self.UIFont = pygame.font.SysFont(None, 48)
        self.FloorFont = pygame.font.SysFont(None, 96)
        
        self.previousFloorText = self.FloorFont.render(f"F{self.game.game_data['floor'] - 1}", False, (255,255,255))
        self.previousFloorTextPos = WINDOW_HEIGHT / 2

        self.nextFloorText = self.FloorFont.render(f"F{self.game.game_data['floor']}", False, (255,255,255))
        self.nextFloorTextPos = WINDOW_HEIGHT * 1.75

        #############################
        # Load the elevator
        #############################
        self.elevatorRoom = Room(OgmoMap(), (0,0))

        self.canSkip = self.game.game_data['floor'] > 2 and self.game.game_data['floor'] != 15

        self.music_timing = 0
        self.elevator_music_sfx: pygame.mixer.Sound | None = None


    def exit(self):
        pass

    def handle_events(self, events):

        # instant presses
        for event in events:

            # JOYSTICKS
            if event.type == pygame.JOYBUTTONUP:

                # player2 joining by pressing start, spawns at p1 pos
                if event.button == self.game.input_maps[event.joy]["START"] and event.joy == 1:
                    if len(self.Players) == 1:
                        self.Players.append(Player(2, self.Players[0].Rect.x, self.Players[0].Rect.y))

            if self.canSkip:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.skipTonextFloor()

                if event.type == pygame.JOYBUTTONUP:
                    if event.button == self.game.input_maps[event.joy]["START"] and event.joy == 0:
                        self.skipTonextFloor()

        ######################################
        # CONTINUOUS INPUT (MOVEMENT)
        ######################################

        # KEYBOARD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: #or keys[K_a]:
            self.Players[0].MoveLeft(self.elevatorRoom.Obstacles)
        elif keys[pygame.K_RIGHT]: #or keys[K_d]:
            self.Players[0].MoveRight(self.elevatorRoom.Obstacles)
        if keys[pygame.K_UP]: #or keys[K_w]:
            self.Players[0].MoveUp(self.elevatorRoom.Obstacles)
        elif keys[pygame.K_DOWN]: #or keys[K_s]:
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

    def skipTonextFloor(self):
        if self.elevator_music_sfx is not None:
            self.elevator_music_sfx.stop()
        if self.game.game_data['floor'] not in [11,12,13,14]: # todo sfx for those floors
            SFXFactory.PlayElevatorFloorAnouncementSFX(self.game.game_data['floor'])
        self.moveToNextState()


    def update(self, dt: float):

        self.music_timing += dt
        if self.music_timing >= 1 and self.elevator_music_sfx is None:
            self.elevator_music_sfx = SFXFactory.PlayElevatorMusicSFX()

        # raise everything
        self.YOffset += self.scrollingSpeed * dt
        self.floorRect = pygame.Rect(self.XOffset + 64, self.YOffset + 64, 300, 236)
        self.previousFloorTextPos += self.scrollingSpeed * dt
        self.nextFloorTextPos += self.scrollingSpeed * dt

        # end of animation
        if self.YOffset <= -360:
            if self.game.game_data['floor'] not in [11,12,13,14]: # todo sfx for those floors
                SFXFactory.PlayElevatorFloorAnouncementSFX(self.game.game_data['floor'])
            self.moveToNextState()

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
    
        # Floor numbers
        screen.blit(self.previousFloorText, (700, self.previousFloorTextPos))
        screen.blit(self.nextFloorText, (700, self.nextFloorTextPos))
        
        if self.canSkip:
            font = pygame.font.SysFont(None, 24)
            text = font.render('(Press space or start to skip)', True, (255, 255, 255))
            screen.blit(text, (WINDOW_WIDTH / 2 - text.get_width()/ 2, 20))

    def moveToNextState(self):
        self.game.change_state("Story" if self.game.game_data['floor'] == 15 else "Action")
        