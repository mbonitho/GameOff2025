from gamestates.gameState import GameState
import pygame


# Splash screen state
class SplashState(GameState):
    def enter(self):
        print("Entered Splash State")
        self.LogoSurface = pygame.image.load('assets/sprites/cool_poop.png').convert_alpha()
        self.logoX = self.game.GAME_WINDOW_SIZE[0] / 2 - self.LogoSurface.get_width() / 2
        self.logoY = self.game.GAME_WINDOW_SIZE[1] / 2 - self.LogoSurface.get_height() / 2

        self.game.splash_timer = 3

    def update(self, dt: float):
        # Simulate splash duration
        self.game.splash_timer -= dt
        if self.game.splash_timer <= 0:
            self.game.change_state("Title")

    def draw(self, screen):
        screen.fill((72, 55, 55))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Cool Poop.", True, (255, 255, 255))
        screen.blit(text, (self.logoX + self.LogoSurface.get_width() / 2 - text.get_width() / 2 + 30, self.logoY + self.LogoSurface.get_height() + 32))

        screen.blit(self.LogoSurface, (self.logoX, self.logoY))