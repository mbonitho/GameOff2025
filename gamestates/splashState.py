from gamestates.gameState import GameState
import pygame


# Splash screen state
class SplashState(GameState):
    def enter(self):
        print("Entered Splash State")

    def update(self, dt: float):
        # Simulate splash duration
        self.game.splash_timer -= dt
        if self.game.splash_timer <= 0:
            self.game.change_state("Title")

    def draw(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 48)
        text = font.render("Splash Screen", True, (255, 255, 255))
        screen.blit(text, (100, 100))
