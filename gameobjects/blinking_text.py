

from typing import Tuple
import pygame


class BlinkingText:

    def __init__(self, text: str, pos: Tuple[int, int], font_size: int = 24, tint: Tuple[int, int] = (255, 255, 255)):
        self.visible = True
        self.blinking_timer = 0
        self.blinking_speed = 1 # s

        self.font = pygame.font.SysFont(None, font_size)
        self.renderedText = self.font.render(text, False, tint)
        self.tint = tint
        self.text = text

        self.position = pos
        

    def renderNewText(self, newText: str):
        if newText != self.text:
            self.renderedText = self.font.render(newText, False, self.tint) 
    
    def update(self, dt: float):
        self.blinking_timer += dt

        if self.blinking_timer > self.blinking_speed:
            self.blinking_timer %= self.blinking_speed
            self.visible = not self.visible


    def draw(self, screen):
        if self.visible:
            screen.blit(self.renderedText, self.position)