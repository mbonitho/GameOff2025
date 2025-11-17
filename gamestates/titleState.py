import pygame
from gamestates.gameState import GameState
from pygame.locals import *

# Title screen state
class TitleState(GameState):
    def enter(self):
        print("Entered Title State")
        self.TitleSurface = pygame.image.load('assets/sprites/environment/backgrounds/titleBG.png').convert_alpha()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    self.game.change_state("Action")

            if event.type == pygame.JOYBUTTONUP:
                if event.button == 7:
                    self.game.change_state("Action")

    def draw(self, screen):
        screen.fill((30, 30, 60))

        screen.blit(self.TitleSurface, (0,0))

        # title_font = pygame.font.SysFont(None, 64)
        # title_text = title_font.render("TEMPLATE GAME", True, (255, 255, 255))
        # screen.blit(title_text, (100, 100))


        subtitle_font = pygame.font.SysFont(None, 96)
        subtitle_text = subtitle_font.render("Press Space to start", True, (255, 255, 255))
        screen.blit(subtitle_text, (600, 800))

        # highscore_font = pygame.font.SysFont(None, 24)
        # score_text = highscore_font.render(f'High score: {self.game.game_data['highscore']}', True, (255, 255, 255))
        # screen.blit(score_text, (500, 440))