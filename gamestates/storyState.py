import pygame
from gamestates.gameState import GameState
from pygame.locals import *

from utils.parameters import POPUP_TEXTS, WINDOW_HEIGHT, WINDOW_WIDTH

# Story screen state
class StoryState(GameState):
    def enter(self):
        print("Entered Story State")
        self.BGSurface = pygame.image.load('assets/sprites/environment/backgrounds/titleBG.png').convert_alpha()

        self.linesX = 200
        self.linesY = WINDOW_HEIGHT

        # determine lines
        self.lines = []
        if self.game.game_data['floor'] == 1:
            self.lines = POPUP_TEXTS['INTRO']
        elif self.game.game_data['floor'] == 15:
            self.lines = POPUP_TEXTS['BEFORE_FINAL_BOSS']

        self.endY = self.linesY - len(self.lines) * 40 - WINDOW_HEIGHT * .5
        pass


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

        screen.blit(self.BGSurface, (0,0))

        overlay = pygame.Surface((WINDOW_WIDTH - 200, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, 
                         (0, 0, 0, 150), 
                         pygame.Rect(100, 0, WINDOW_WIDTH - 200, WINDOW_HEIGHT))
        screen.blit(overlay, (100, 0))

        lineY = self.linesY
        font = pygame.font.SysFont(None, 32)
        for line in self.lines:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (self.linesX, lineY))
            lineY += 40

        font = pygame.font.SysFont(None, 24)
        text = font.render('(Press space or start to skip)', True, (255, 255, 255))
        screen.blit(text, (WINDOW_WIDTH - text.get_width() - 20, 20))


    def update(self, dt: float):
        if self.linesY >= self.endY:
            self.linesY -= 24 * dt
