from gamestates.gameState import GameState
import pygame
from pygame.locals import *
import random

class GameplayState(GameState):

    def enter(self):
        print("Entered Gameplay State")
        self.bird_y = 240
        self.bird_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -8
        self.pipe_gap = 150
        self.pipe_width = 80
        self.pipe_speed = 3
        self.pipes = []
        self.spawn_pipe()
        self.game.game_data['score'] = 0
        self.font = pygame.font.SysFont(None, 48)

    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.bird_velocity = self.jump_strength

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == self.game.input_map["jump"]:
                    self.bird_velocity = self.jump_strength
            

    def update(self, dt):
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity

        # Move pipes
        for pipe in self.pipes:
            pipe["x"] -= self.pipe_speed

        # Remove off-screen pipes and spawn new ones
        if self.pipes and self.pipes[0]["x"] < -self.pipe_width:
            self.pipes.pop(0)
            self.spawn_pipe()
            self.game.game_data['score'] += 1

        # Collision detection
        bird_rect = pygame.Rect(100, int(self.bird_y), 40, 40)
        for pipe in self.pipes:
            top_rect = pygame.Rect(pipe["x"], 0, self.pipe_width, pipe["top"])
            bottom_rect = pygame.Rect(pipe["x"], pipe["bottom"], self.pipe_width, 480 - pipe["bottom"])
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                print("Game Over")
                if self.game.game_data['score'] > int(self.game.game_data['highscore']):
                    self.game.game_data['highscore'] = self.game.game_data['score']
                    self.game.save_data()
                self.game.change_state("Title")  

        # Ground and ceiling collision
        if self.bird_y < 0 or self.bird_y > 480:
            print("Game Over")
            if int(self.game.game_data['score']) > int(self.game.game_data['highscore']):
                self.game.game_data['highscore'] = self.game.game_data['score']
                self.game.save_data()
            self.game.change_state("Title") 

    def draw(self, screen):
        screen.fill((135, 206, 250))  # Sky blue

        # Draw bird
        pygame.draw.rect(screen, (255, 255, 0), (100, int(self.bird_y), 40, 40))

        # Draw pipes
        for pipe in self.pipes:
            pygame.draw.rect(screen, (34, 139, 34), (pipe["x"], 0, self.pipe_width, pipe["top"]))
            pygame.draw.rect(screen, (34, 139, 34), (pipe["x"], pipe["bottom"], self.pipe_width, 480 - pipe["bottom"]))

        # Draw score
        text = self.font.render(f"Score: {self.game.game_data['score']}", True, (255, 255, 255))
        screen.blit(text, (20, 20))

    def spawn_pipe(self):
        height = random.randint(100, 300)
        x = 640
        self.pipes.append({
            "x": x,
            "top": height,
            "bottom": height + self.pipe_gap
        })