

from typing import Tuple
import pygame


class BlinkingText:

    def __init__(self, text: str, pos: Tuple[int, int], font_size: int = 24, tint: Tuple[int, int] = (255, 255, 255)):
        self.visible = True
        self.blinking_timer = 0
        self.blinking_speed = 1 # s

        self.font = pygame.font.SysFont(None, font_size)
        self.text = self.font.render(text, False, tint)

        self.position = pos
        

    
    def update(self, dt: float):
        self.blinking_timer += dt

        if self.blinking_timer > self.blinking_speed:
            self.blinking_timer %= self.blinking_speed
            self.visible = not self.visible


    def draw(self, screen):
        if self.visible:
            screen.blit(self.text, self.position)