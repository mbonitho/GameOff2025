from pygame import Rect, Surface
from typing import Tuple
from utils.helpers.collisions_helper import MoveAndCollide

class Player:

    def __init__(self, surface: Surface, x: int, y: int, color: Tuple[int, int, int]):
        self.Surface = surface
        self.Rect = surface.get_rect()
        self.Rect.topleft = (x, y)
        self.Tint = color

        self.Speed = 6
        self.MaxLife = 5
        self.Life = self.MaxLife
        self.Score = 0

        self.MaxBullets = 3
        self.Bullets = []

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

    def MoveX(self, value, obstacles: list[Rect]):
        #self.Rect.x += self.Speed * value
        MoveAndCollide(self.Rect, self.Speed * value, 0, obstacles)

    def MoveY(self, value, obstacles: list[Rect]):
        #self.Rect.y += self.Speed * value
        MoveAndCollide(self.Rect, 0, self.Speed * value, obstacles)

    def MoveLeft(self, obstacles: list[Rect], ratio: float = 1):
        #self.Rect.x -= int(self.Speed * ratio)
        MoveAndCollide(self.Rect, int(self.Speed * ratio) * -1, 0, obstacles)


    def MoveRight(self, obstacles: list[Rect], ratio: float = 1):
        #self.Rect.x += int(self.Speed * ratio)
        MoveAndCollide(self.Rect, int(self.Speed * ratio), 0, obstacles)

    def MoveUp(self, obstacles: list[Rect], ratio: float = 1):
        #self.Rect.y -= int(self.Speed * ratio)
        MoveAndCollide(self.Rect, 0, int(self.Speed * ratio) * -1, obstacles)

    def MoveDown(self, obstacles: list[Rect], ratio: float = 1):
        #self.Rect.y += int(self.Speed * ratio)
        MoveAndCollide(self.Rect, 0, int(self.Speed * ratio), obstacles)

    def ReceiveDamage(self):
        # invicibility fames
        if self.overall_blinking_timer < 0:
            self.overall_blinking_timer = 0
            self.Life -= 1

    def TryShootBullet(self, bullet):

        if len(self.Bullets) < self.MaxBullets:
            self.Bullets.append(bullet)