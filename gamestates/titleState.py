import pygame
from gameobjects.blinkingComponent import BlinkingComponent
from gamestates.gameState import GameState
from pygame.locals import *
import random

from utils.parameters import WINDOW_HEIGHT, WINDOW_WIDTH
from utils.sfx_factory import SFXFactory

# Title screen state
class TitleState(GameState):
    def enter(self):
        self.TitleBGSurface = pygame.image.load('assets/sprites/environment/backgrounds/titleBG.png').convert()
        self.TitleLogo1Surface = pygame.image.load('assets/sprites/environment/title/titleLogo1.png').convert_alpha()
        self.TitleLogo2Surface = pygame.image.load('assets/sprites/environment/title/titleLogo2.png').convert_alpha()
        self.TitleLightningSurface = pygame.image.load('assets/sprites/environment/title/titleScreenLightning.png').convert_alpha()
        
        self.blinkingComponent = BlinkingComponent()
        self.blinkingComponent.total_blinking_duration = .5
        self.blinkingComponent.blinking_speed = .075
        
        self.blinking_delay = random.randint(1,5)
        self.waited_time = 0

        self.pressStartY = 600
        self.pressStartDirection = 1

        self.game.PlayBGM('title')

        ###############################################
        # PRERENDER TO OPTIMIZE PERFORMANCE ON THE WEB
        ###############################################
        if self.game.WEB:
            # lower BG image quality to improve performance on the web
            self.TitleBGSurface = pygame.transform.scale(self.TitleBGSurface, (640, 480))
            self.TitleBGSurface = pygame.transform.scale(self.TitleBGSurface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title_font = pygame.font.SysFont(None, 32)
        self.title_text = self.title_font.render("2025, Mathieu Bonithon & Gael Rincon", True, (255, 255, 255))
        self.credits_text = self.title_font.render("Press C to view the full credits", True, (255, 255, 255))
        self.completion_time_text = self.title_font.render(f'Your completion time is: {self.game.str_final_time}', True, (255, 255, 255))
        self.toggle_fullscreen_text = self.title_font.render('Press F11 to toggle Fullscreen mode', True, (255, 255, 255))
        self.subtitle_font = pygame.font.SysFont(None, 64)
        self.subtitle_text = self.subtitle_font.render("Press Space or Start to begin", True, (255, 255, 255))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    self.start_game()

                if event.key == K_c:
                    SFXFactory.PlayM9SFX()
                    self.game.change_state("Credits")


            if event.type == pygame.JOYBUTTONUP:
                if event.button == self.game.input_maps[event.joy]["START"]:
                    self.start_game()


    def start_game(self):
        # start chronometer
        if self.game.game_data['floor'] == 1:
            self.game.current_run_time = 0
        SFXFactory.PlayWeeeeeSFX()
        self.game.change_state("Story" if self.game.game_data['floor'] == 1 else "Action")
        
    def draw(self, screen):
        screen.fill((30, 30, 60))

        screen.blit(self.TitleBGSurface, (0,0))

        # title logo and lightning (blinking)
        if not self.blinkingComponent.visible:
            screen.blit(self.TitleLightningSurface, (540, 140))
            screen.blit(self.TitleLogo2Surface, (680, 130))
        else:
            screen.blit(self.TitleLogo1Surface, (680, 130))

        screen.blit(self.title_text, (850, 880))
        screen.blit(self.credits_text, (850, 920))
        screen.blit(self.subtitle_text, (340, self.pressStartY))

        # if the game was beaten at least once, display last win time
        if self.game.str_final_time != '':
            screen.blit(self.completion_time_text, (20, 880))
        if not self.game.WEB:
            screen.blit(self.toggle_fullscreen_text, (20, 920))

    def update(self, dt: float):

        self.blinkingComponent.update(dt)

        self.pressStartY += self.pressStartDirection * dt * 4 
        if self.pressStartY <= 598 or self.pressStartY >= 602:
            self.pressStartDirection *= -1

        self.waited_time += dt
        if self.waited_time >= self.blinking_delay:
            self.waited_time %= self.blinking_delay
            self.blinking_delay = random.randint(2,7)

            self.blinkingComponent.StartBlinking()

