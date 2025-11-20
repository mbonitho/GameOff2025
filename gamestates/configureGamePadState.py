from gamestates.gameState import GameState
import pygame


# Config screen state
class ConfigureGamePadState(GameState):
    def enter(self):
        print("Entered Config State")

    def update(self, dt: float):
        pass

    def draw(self, screen):
        screen.fill((72, 55, 55))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Cool Poop.", True, (255, 255, 255))
        screen.blit(text, (self.logoX + self.LogoSurface.get_width() / 2 - text.get_width() / 2 + 30, self.logoY + self.LogoSurface.get_height() + 32))

        screen.blit(self.LogoSurface, (self.logoX, self.logoY))