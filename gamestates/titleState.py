import pygame
from gameobjects.blinkingComponent import BlinkingComponent
from gamestates.gameState import GameState
from pygame.locals import *
import random

# Title screen state
class TitleState(GameState):
    def enter(self):
        print("Entered Title State")
        self.TitleBGSurface = pygame.image.load('assets/sprites/environment/backgrounds/titleBG.png').convert_alpha()
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

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    self.game.change_state("Story" if self.game.game_data['floor'] == 1 else "Action")

            if event.type == pygame.JOYBUTTONUP:
                if event.button == self.game.input_maps[event.joy]["START"]:
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
            
        # about
        title_font = pygame.font.SysFont(None, 32)
        title_text = title_font.render("2025, Mathieu Bonithon & Gael Rincon", True, (255, 255, 255))
        screen.blit(title_text, (850, 920))

        # buttons
        subtitle_font = pygame.font.SysFont(None, 64)
        subtitle_text = subtitle_font.render("Press Space or Start to begin", True, (255, 255, 255))
        screen.blit(subtitle_text, (340, self.pressStartY))


        # highscore_font = pygame.font.SysFont(None, 24)
        # score_text = highscore_font.render(f'High score: {self.game.game_data['highscore']}', True, (255, 255, 255))
        # screen.blit(score_text, (500, 440))

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

