import pygame
from gamestates.gameState import GameState
from pygame.locals import *

# Title screen state
class TitleState(GameState):
    def enter(self):
        print("Entered Title State")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    self.game.change_state("Gameplay")

    def draw(self, screen):
        screen.fill((30, 30, 60))

        title_font = pygame.font.SysFont(None, 64)
        title_text = title_font.render("TEMPLATE GAME", True, (255, 255, 255))
        screen.blit(title_text, (100, 100))


        subtitle_font = pygame.font.SysFont(None, 32)
        subtitle_text = subtitle_font.render("Press Space to start", True, (255, 255, 255))
        screen.blit(subtitle_text, (100, 300))

        highscore_font = pygame.font.SysFont(None, 24)
        score_text = highscore_font.render(f'High score: {self.game.game_data['highscore']}', True, (255, 255, 255))
        screen.blit(score_text, (500, 440))