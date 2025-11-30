import pygame
from gamestates.gameState import GameState
from pygame.locals import *

from utils.parameters import POPUP_TEXTS, WINDOW_HEIGHT, WINDOW_WIDTH
from utils.sfx_factory import SFXFactory

# Story screen state
class StoryState(GameState):
    def enter(self):
        self.BGSurface = pygame.image.load('assets/sprites/environment/backgrounds/titleBG.png').convert_alpha()

        self.linesX = 200
        self.linesY = WINDOW_HEIGHT

        # determine the state after this story segment
        self.target_state = "Action" if self.game.game_data['floor'] != 16 else "Title"

        # determine lines
        self.lines = []
        if self.game.game_data['floor'] == 1:
            self.lines = POPUP_TEXTS['INTRO']
        elif self.game.game_data['floor'] == 15:
            self.lines = POPUP_TEXTS['BEFORE_FINAL_BOSS']
        elif self.game.game_data['floor'] == 16:
            self.lines = POPUP_TEXTS['AFTER_FINAL_BOSS']
            self.lines.append(f'Your completion time is: {self.game.str_final_time}')
            self.game.game_data['floor'] = 1 # resets the game progression

        self.endY = self.linesY - len(self.lines) * 40 - WINDOW_HEIGHT * .5
        
        self.skip_timing = -1


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    SFXFactory.PlayM9SFX()
                    self.skip_timing = 0
            if event.type == pygame.JOYBUTTONUP:
                if event.button == self.game.input_maps[event.joy]["START"]:
                    SFXFactory.PlayM9SFX()
                    self.skip_timing = 0

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

        if self.skip_timing >= 0:
            self.skip_timing += dt

            if self.skip_timing >= 0.5:
                self.game.change_state(self.target_state)


        if self.linesY >= self.endY:
            self.linesY -= 24 * dt
