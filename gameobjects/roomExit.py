from pygame import Rect

class RoomExit:

    def __init__(self, rect: Rect, dir: str):
        self.Rect = rect
        self.Direction = dir