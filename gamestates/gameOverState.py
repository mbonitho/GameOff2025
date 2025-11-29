import pygame
from gameobjects.blinking_text import BlinkingText
from gameobjects.weapons.weapons_factory import WeaponFactory
from gamestates.gameState import GameState
from pygame.locals import *

# Game Over screen state
class GameOverState(GameState):
    def enter(self):
        print("Entered Title State")
        self.BGSurface = pygame.image.load('assets/sprites/environment/backgrounds/titleBG.png').convert_alpha()
        self.GameOverSurface = pygame.image.load('assets/sprites/environment/gameover/gameOver.png').convert_alpha()

        self.GameOverSurfaceY = -535

        self.RetryText = BlinkingText("Press Space or Start to restart", (400, 900), 48)


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    self.continueGame()

            if event.type == pygame.JOYBUTTONUP:
                if event.button == self.game.input_maps[event.joy]["START"]:
                    self.continueGame()

    def draw(self, screen):
        screen.fill((30, 30, 60))

        screen.blit(self.BGSurface, (0,0))

        screen.blit(self.GameOverSurface, (750, self.GameOverSurfaceY))

        self.RetryText.draw(screen)

        # highscore_font = pygame.font.SysFont(None, 24)
        # score_text = highscore_font.render(f'High score: {self.game.game_data['highscore']}', True, (255, 255, 255))
        # screen.blit(score_text, (500, 440))

    def update(self, dt: float):
        self.RetryText.update(dt)
        if self.GameOverSurfaceY < 350:
            self.GameOverSurfaceY += 800 * dt

    def continueGame(self):
        for p in self.game.players:
            p.CurrentLife = p.MaxLife
            p.Weapon = WeaponFactory.GetDefaultWeapon(p)
            
        self.game.change_state("Action")