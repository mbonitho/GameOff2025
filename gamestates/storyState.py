import pygame
from gamestates.gameState import GameState

from utils.parameters import POPUP_TEXTS, WINDOW_HEIGHT, WINDOW_WIDTH
from utils.sfx_factory import SFXFactory

# Story screen state
class StoryState(GameState):
    def enter(self):

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
                if event.key == pygame.K_SPACE:
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

            if self.skip_timing >= 1:
                self.game.change_state(self.target_state)


        if self.linesY >= self.endY:
            self.linesY -= 24 * dt
