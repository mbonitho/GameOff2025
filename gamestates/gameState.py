# Base class for all game states
class GameState:
    def __init__(self, game):
        self.game = game

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_events(self, events):
        pass

    def update(self, dt: float):
        pass

    def draw(self, screen):
        pass
