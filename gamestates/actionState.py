
import random
import pygame
from pygame.locals import *

from gameobjects.blinking_text import BlinkingText
from gameobjects.bullet import Bullet
from gameobjects.enemies.seek_nearest_player_behavior import SeekNearestPlayerBehavior
from gameobjects.player import Player
from gameobjects.enemies.enemy import Enemy
from gamestates.gameState import GameState
from utils.helpers.surface_helper import tint_surface


class ActionState(GameState):

    def enter(self):
        print("Entered Action State")

        #############################
        # SURFACES
        #############################
        self.BulletSurface = pygame.image.load('assets/sprites/bullet.png').convert_alpha()
        self.EnemySurface = pygame.image.load('assets/sprites/enemies/enemy_1.png').convert_alpha()

        #############################
        # ENTITIES
        #############################
        p1_surf = tint_surface(pygame.image.load('assets/sprites/player/player_1.png').convert_alpha(), (23,45,34))
        self.Players = [Player(p1_surf, 100, 100, (23,45,34))]
        self.Bullets = []

        #############################
        # UI
        #############################
        self.UIFont = pygame.font.SysFont(None, 24)
        self.player2PressStartText = BlinkingText('Player 2 - press start', (self.game.screen.get_width() - 200, 16))

        #############################
        # Load a bunch of enemies (to remove later)
        #############################
        self.enemySpawningTimer = 0
        self.enemySpawnDelay = 3 # seconds
        self.Enemies = []


    def exit(self):
        pass

    def handle_events(self, events):

        # instant presses
        for event in events:

            # KEYBOARD
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    pass

            # JOYSTICKS
            if event.type == pygame.JOYBUTTONUP:
                print(f"Joystick {event.joy} Button {event.button} released")

                # player2 joining by pressing start, spawns at p1 pos
                if event.button == 7 and event.joy == 1:
                    if len(self.Players) == 1:
                        p2_surf = tint_surface(pygame.image.load('assets/sprites/player/player_1.png').convert_alpha(), (210,120,72))
                        self.Players.append(Player(p2_surf, self.Players[0].X, self.Players[0].Y, (210,120,72)))

                # only trigger input if the number of players is sufficient
                if event.joy == 0 or (event.joy == 1 and len(self.Players) == 2):
                    
                    if event.button == 2:
                        player = self.Players[event.joy]
                        self.Bullets.append(Bullet(self.BulletSurface, player.X, player.Y, -1, 0))
                    elif event.button == 0:
                        player = self.Players[event.joy]
                        self.Bullets.append(Bullet(self.BulletSurface, player.X, player.Y, 0, 1))
                    elif event.button == 1:
                        player = self.Players[event.joy]
                        self.Bullets.append(Bullet(self.BulletSurface, player.X, player.Y, 1, 0))
                    elif event.button == 3:
                        player = self.Players[event.joy]
                        self.Bullets.append(Bullet(self.BulletSurface, player.X, player.Y, 0, -1))

        ######################################
        # CONTINUOUS INPUT (MOVEMENT)
        ######################################

        # KEYBOARD
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.Players[0].MoveLeft()
        elif keys[K_RIGHT] or keys[K_d]:
            self.Players[0].MoveRight()

        if keys[K_UP] or keys[K_w]:
            self.Players[0].MoveUp()

        elif keys[K_DOWN] or keys[K_s]:
            self.Players[0].MoveDown()

        # GAMEPADS 
        for index, player in enumerate(self.Players):

            if len(self.game.joysticks) > index:

                joy = self.game.joysticks[index]

                axis_x_val = joy.get_axis(0)
                axis_y_val = joy.get_axis(1)


                # Dead zone" to prevent jitter and drift
                dead_zone_threshold = 0.1

                if abs(axis_x_val) > dead_zone_threshold:
                    player.MoveX(axis_x_val)

                if abs(axis_y_val) > dead_zone_threshold:
                    player.MoveY(axis_y_val)

                if joy.get_hat(0)[0] != 0:
                    player.MoveX(joy.get_hat(0)[0])

                if joy.get_hat(0)[1] != 0:
                    player.MoveY(joy.get_hat(0)[1] * -1)


    def update(self, dt: float):

        # blinking text
        if len(self.Players) == 1:
            self.player2PressStartText.update(dt)

        # Update enemies
        for enemy in self.Enemies:
            enemy.update(self.Players, dt)

        # Update bullets
        for bullet in self.Bullets.copy():
            bullet.update(self.Enemies, dt)
            if bullet.lifespan >= bullet.max_lifespan:
                self.Bullets.remove(bullet)

        # Spawn enemies
        self.enemySpawningTimer += dt
        if self.enemySpawningTimer >= self.enemySpawnDelay:
            self.enemySpawningTimer %= self.enemySpawnDelay

            for i in range(4 * len(self.Players)):
                x = 0
                y = 0
                rng = random.randint(1, 4)
                match(rng):
                    case 1: # TOP OF SCREEN
                        x = random.randrange(int(self.game.screen.get_width() * 0.25), int(self.game.screen.get_width() * 0.75))
                        y = -self.EnemySurface.get_height()
                    case 2: # BOTTOM OF SCREEN
                        x = random.randrange(int(self.game.screen.get_width() * 0.25), int(self.game.screen.get_width() * 0.75))
                        y = self.game.screen.get_height() + self.EnemySurface.get_height() 
                    case 3: # LEFT OF SCREEN
                        x = -self.EnemySurface.get_width()
                        y = random.randrange(int(self.game.screen.get_height() * 0.25), int(self.game.screen.get_height() * 0.75))
                    case 4: # RIGHT OF SCREEN
                        x = self.game.screen.get_width() + self.EnemySurface.get_width()
                        y = random.randrange(int(self.game.screen.get_height() * 0.25), int(self.game.screen.get_height() * 0.75))

                self.Enemies.append(
                    Enemy(
                        self.EnemySurface, 
                        x,
                        y,
                        [SeekNearestPlayerBehavior()]
                    )
                )

        # check for game over
        continueGame = any(p.Life > 0 for p in self.Players)
        if not continueGame:
            self.game.change_state("GameOver")

    def draw(self, screen):
        screen.fill((64, 64, 64))

        for p in self.Players:
            screen.blit(p.Surface, (p.X, p.Y))

        for e in self.Enemies:
            e.draw(screen)

        for bullet in self.Bullets:
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