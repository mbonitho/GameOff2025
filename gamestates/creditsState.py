import pygame
from gamestates.gameState import GameState
from pygame.locals import *

from utils.parameters import WINDOW_HEIGHT, WINDOW_WIDTH
from utils.sfx_factory import SFXFactory

# Story screen state
class CreditState(GameState):
    def enter(self):
        print("Entered Credit State")
        self.BGSurface = pygame.image.load('assets/sprites/environment/backgrounds/titleBG.png').convert_alpha()

        self.linesX = 200
        self.linesY = WINDOW_HEIGHT

        # determine lines
        self.lines = [
            "Project W.A.V.E.S - Where All Victims End Silently",
            "",
            "Mathieu Bonithon - Code & Game design",
            "Gael Rincon - Sound design & Game design",
            "",
            "Music used:",
            "Horror unsettling victory loop, by Clement Panchout",
            "https://opengameart.org/content/horror-unsettling-victory-loop",
            "",
            "Sinister loop, by Patrick Maney",
            "https://opengameart.org/content/sinister-loop",
            "",
            "Technovillain, by Joth",
            "https://opengameart.org/content/technovillain-0",
            "",
            "Demon Lord, by Scrabbit",
            "https://opengameart.org/content/demon-lord",
            "",
            "One, by pheonton"
            "https://opengameart.org/content/one"
        ]


        self.endY = self.linesY - len(self.lines) * 40 - WINDOW_HEIGHT * .25
        
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
        text = font.render('(Press space or start to return to the title screen)', True, (255, 255, 255))
        screen.blit(text, (WINDOW_WIDTH - text.get_width() - 20, 20))


    def update(self, dt: float):

        if self.skip_timing >= 0:
            self.skip_timing += dt

            if self.skip_timing >= 0.5:
                self.game.change_state("Title")


        if self.linesY >= self.endY:
            self.linesY -= 48 * dt
