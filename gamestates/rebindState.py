from gamestates.gameState import GameState
import pygame
from pygame.locals import *

class RebindMenuState(GameState):
    def enter(self):
        print("Entered Rebind Menu State")
        self.actions = ["jump", "pause"]
        self.current_action_index = 0
        self.awaiting_input = True
        self.font = pygame.font.SysFont(None, 36)
        self.message = f"Press a button to bind '{self.actions[self.current_action_index]}'"

    def handle_events(self, events):
        if not self.awaiting_input:
            return

        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                action = self.actions[self.current_action_index]
                self.game.input_map[action] = event.button
                print(f"Bound '{action}' to button {event.button}")
                self.current_action_index += 1

                if self.current_action_index < len(self.actions):
                    self.message = f"Press a button to bind '{self.actions[self.current_action_index]}'"
                else:
                    self.awaiting_input = False
                    self.message = "All actions bound! Press Enter to return."
                    self.game.save_inputmap()

            elif event.type == KEYDOWN and event.key == K_RETURN and not self.awaiting_input:
                self.game.change_state("Title")

    def update(self, dt):
        pass  # No dynamic updates needed

    def draw(self, screen):
        screen.fill((50, 50, 80))
        text = self.font.render("Controller Rebinding", True, (255, 255, 255))
        prompt = self.font.render(self.message, True, (200, 200, 200))
        screen.blit(text, (100, 100))
        screen.blit(prompt, (100, 160))
