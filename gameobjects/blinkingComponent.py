from pygame import Rect, Surface
from typing import Tuple
from utils.helpers.collisions_helper import MoveAndCollide

class BlinkingComponent:

    def __init__(self):
        self.visible = True
        self.overall_blinking_timer = -1
        self.total_blinking_duration = 1.5 #s
        self.blinking_timer = 0
        self.blinking_speed = .15 # seconds


    def update(self, dt: float):
        
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

    def IsBlinking(self) -> bool:
        return self.overall_blinking_timer >= 0
    

    def StartBlinking(self):
        self.overall_blinking_timer = 0
