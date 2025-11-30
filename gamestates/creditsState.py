import pygame
from gamestates.gameState import GameState
from pygame.locals import *

from utils.parameters import WINDOW_HEIGHT, WINDOW_WIDTH
from utils.sfx_factory import SFXFactory

# Story screen state
class CreditState(GameState):
    def enter(self):
        self.BGSurface = pygame.image.load('assets/sprites/environment/backgrounds/titleBG.png').convert_alpha()

        self.linesX = 200
        self.linesY = WINDOW_HEIGHT

        # determine lines
        self.lines = [
            "Project W.A.V.E.S - Where All Victims End Silently",
            "",
            "Made in a month for GitHub GameOff 2025",
            "",
            "Mathieu Bonithon - Code, Graphics & Game design",
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
            "One, by pheonton",
            "https://opengameart.org/content/one"
        ]


        self.endY = self.linesY - len(self.lines) * 40 - WINDOW_HEIGHT * .25
        
        self.skip_timing = -1

        ###############################################
        # PRERENDER TO OPTIMIZE PERFORMANCE ON THE WEB
        ###############################################

        # Prerender BG once
        self.BGSurface = pygame.image.load('assets/sprites/environment/backgrounds/titleBG.png').convert()
        if self.game.WEB:
            # lower image quality to improve performance on the web
            self.BGSurface = pygame.transform.scale(self.BGSurface, (640, 480))
            self.BGSurface = pygame.transform.scale(self.BGSurface, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # prerender fonts once
        self.lines_font = pygame.font.SysFont(None, 32)
        self.skip_font = pygame.font.SysFont(None, 24)

        # prerender overlay once
        self.overlay = pygame.Surface((WINDOW_WIDTH - 200, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(self.overlay, 
                         (0, 0, 0, 150), 
                         pygame.Rect(100, 0, WINDOW_WIDTH - 200, WINDOW_HEIGHT))

        # prerender lines
        color = (255,255,255) if not self.game.WEB else (255,0,0)
        self.lines_surfaces = [
            self.lines_font.render(line, True, color)
            for line in self.lines
        ]
        self.skip_surface = self.skip_font.render('(Press space or start to skip)', True, (255, 255, 255))


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

        self.game.render_surface.blit(self.BGSurface, (0,0))
        if not self.game.WEB:
            self.game.render_surface.blit(self.overlay, (100, 0))

        lineY = self.linesY
        for surf in self.lines_surfaces:
            screen.blit(surf, (self.linesX, lineY))
            lineY += 40

        screen.blit(self.skip_surface, (WINDOW_WIDTH - self.skip_surface.get_width() - 20, 20))


    def update(self, dt: float):

        if self.skip_timing >= 0:
            self.skip_timing += dt

            if self.skip_timing >= 0.5:
                self.game.change_state("Title")


        if self.linesY >= self.endY:
            self.linesY -= 48 * dt
