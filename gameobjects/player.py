from pygame import Surface
from typing import Tuple

class Player:

    def __init__(self, surface: Surface, x: int, y: int, color: Tuple[int, int, int]):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)
        self.Tint = color

        self.Speed = 3
        self.MaxLife = 5
        self.Life = self.MaxLife
        self.Score = 0

        # blinking
        self.visible = True
        self.overall_blinking_timer = -1
        self.total_blinking_duration = 1.5 #s
        self.blinking_timer = 0
        self.blinking_speed = .15 # s


    def update(self, dt: float):
        
        ##########################
        # BLINKING
        ##########################
        if self.overall_blinking_timer >= 0:

            if self.overall_blinking_timer == 0:
                self.blinking_timer = 0

            self.overall_blinking_timer += dt
            self.blinking_timer += dt
            if self.blinking_timer >= self.blinking_speed:
                self.blinking_timer %= self.blinking_speed
                self.visible = not self.visible

            if self.overall_blinking_timer >= self.total_blinking_duration:
                self.blinking_timer = -1
                self.overall_blinking_timer = -1
                self.visible = True


    def draw(self, screen):
        if self.visible:
            screen.blit(self.Surface, self.Rect.topleft)

    def MoveX(self, value):
        self.Rect.x += self.Speed * value

    def MoveY(self, value):
        self.Rect.y += self.Speed * value

    def MoveLeft(self, ratio: float = 1):
        self.Rect.x -= self.Speed * ratio

    def MoveRight(self, ratio: float = 1):
        self.Rect.x += self.Speed * ratio

    def MoveUp(self, ratio: float = 1):
        self.Rect.y -= self.Speed * ratio

    def MoveDown(self, ratio: float = 1):
        self.Rect.y += self.Speed * ratio

    def ReceiveDamage(self):
        # invicibility fames
        if self.overall_blinking_timer < 0:
            self.overall_blinking_timer = 0
            self.Life -= 1