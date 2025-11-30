import sys
import os
import pygame
from pygame.locals import *

from typing import Dict, Optional
from gamestates.actionState import ActionState
from gamestates.creditsState import CreditState
from gamestates.gameOverState import GameOverState
from gamestates.gameState import GameState
from gamestates.splashState import SplashState
from gamestates.storyState import StoryState
from gamestates.titleState import TitleState
from gamestates.elevatorState import ElevatorState
from utils.parameters import INPUT_MAPS, STARTING_FLOOR, STARTING_STATE, WINDOW_HEIGHT, WINDOW_WIDTH

class Game:

    WEB = False
    GAME_WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
    TARGET_ASPECT = WINDOW_WIDTH / WINDOW_HEIGHT

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(Game.GAME_WINDOW_SIZE)
        self.render_surface = pygame.Surface(Game.GAME_WINDOW_SIZE)

        info = pygame.display.get_desktop_sizes()
        self.physical_screen_width, self.physical_screen_height = info[0]

        pygame.display.set_caption("Project W.A.V.E.S")
        self.clock = pygame.time.Clock()
        self.running = True
        self.splash_timer = 0.5  # seconds

        self.states: Dict[str, GameState] = {
            "Splash": SplashState(self),
            "Title": TitleState(self),
            "Action": ActionState(self),
            "GameOver" : GameOverState(self),
            "Elevator" : ElevatorState(self),
            'Story': StoryState(self),
            'Credits': CreditState(self)
        }

        if sys.platform in ['wasi', 'emscripten']:
            Game.WEB = True
            from platform import window
            window.canvas.style.imageRendering = 'pixelated'

        # game settings
        self.is_fullscreen = False
        self.target_width = WINDOW_WIDTH
        self.target_height = WINDOW_HEIGHT

        # clean game data, is overridden when load_data is called
        self.game_data = {
            "highscore": 0,
            "score": 0,
            "floor": STARTING_FLOOR,
            "keyboard_layout": "WASD"
        }

        # gamepad input maps
        self.input_maps = [
            INPUT_MAPS['xbox'],
            INPUT_MAPS['xbox']
        ]        

        self.joysticks = []

        self.players = []

        #finally, set current state
        self.current_state: Optional[GameState] = None
        self.change_state(STARTING_STATE)

        self.current_run_time: float = -1
        self.str_final_time: str = ''

    def load_data(self):
        print('loading data')
        if Game.WEB:
            from platform import window
            for key, value in self.game_data.items():
                self.game_data[key] = str(window.localStorage.getItem(key) or '')
        else:
            if os.path.exists('save'):
                with open('save', 'r') as file:
                    for line in file.readlines():
                        key = line.split('::')[0]
                        value = line.split('::')[1].replace('\n', '')
                        self.game_data[key] = value

    def save_data(self):
        if Game.WEB:
            from platform import window
            for key, value in self.game_data.items():
                window.localStorage.setItem(key, value) 
        else:
            with open('save', 'w') as file:
                for key, value in self.game_data.items():
                    file.write(f'{key}::{value}\n')

    def change_state(self, state_name: str):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[state_name]
        self.current_state.enter()

    def tick(self):
        dt = self.clock.tick(60) / 1000.0
        events = pygame.event.get()

        ########################################
        # MANAGE INPUT
        ########################################
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == KEYDOWN:

                ########################
                # Exit game
                ########################
                if event.key == K_ESCAPE:
                    self.running = False

                ########################
                # Fullscreen!
                ########################
                if event.key == K_F11:
                    self.toggle_fullscreen()

            # Hot-plugging Joysticks 
            if event.type == pygame.JOYDEVICEADDED:
                self.AddAndDetectJoystick(event.device_index)
            if event.type == pygame.JOYDEVICEREMOVED:
                # Re-initialize joysticks or remove the disconnected one from your list
                print(f"Joystick Removed: {event.instance_id}") # instance_id is preferred in Pygame 2.x
                self.joysticks = [j for j in self.joysticks if j.get_instance_id() != event.instance_id]

        ########################################
        # Update time for the current run
        ########################################
        if self.current_run_time >= 0:
            self.current_run_time += dt

        ########################################
        # INPUT, UPDATE, DRAW THE CURRENT STATE
        ########################################
        if self.current_state:
            self.current_state.handle_events(events)
            self.current_state.update(dt)
            self.current_state.draw(self.render_surface)

            if self.is_fullscreen:
                scaled = pygame.transform.scale(
                    self.render_surface, 
                    (self.target_width, self.target_height)
                )
                x = (self.physical_screen_width - self.target_width) // 2
                y = (self.physical_screen_height - self.target_height) // 2
                self.screen.blit(scaled, (x, y))
            
            else:
                self.screen.blit(self.render_surface, (0,0))

        pygame.display.flip()


        if not self.running:
            pygame.mixer.music.stop()
            pygame.quit()

    def toggle_fullscreen(self):
        if not Game.WEB:
            if self.is_fullscreen:
                self.screen = pygame.display.set_mode(Game.GAME_WINDOW_SIZE)
            else:
                import os
                os.environ['SDL_VIDEO_CENTERED'] = '1'
                screen_aspect_ratio = self.physical_screen_width / self.physical_screen_height

                if screen_aspect_ratio > Game.TARGET_ASPECT:
                    # screen is wider than target
                    self.target_height = self.physical_screen_height
                    self.target_width = int(self.target_height * Game.TARGET_ASPECT)
                else:
                    # screen is taller than target
                    self.target_width = self.physical_screen_width
                    self.target_height = int(self.target_width / Game.TARGET_ASPECT)

                self.screen = pygame.display.set_mode(
                                (self.physical_screen_width, self.physical_screen_height), 
                                pygame.NOFRAME)
            self.is_fullscreen = not self.is_fullscreen


    def player1_joystick(self):
        return self.joysticks[0]
    
    def player2_joystick(self):
        return self.joysticks[1]
    
    def AddAndDetectJoystick(self, device_index: int):
        new_joystick = pygame.joystick.Joystick(device_index)
        new_joystick.init()
        self.joysticks.append(new_joystick)
        print(f"New Joystick Added: {new_joystick.get_name()}")

        name = new_joystick.get_name().lower()

        if "xbox" in name:
            layout = "xbox"
        elif "dualshock" in name or "playstation" in name or "dual sense" in name:
            layout = "playstation"
        elif "switch" in name or "nintendo" in name:
            layout = "switch"
        else:
            layout = "generic"
        self.input_maps[device_index] = INPUT_MAPS[layout]


    def PlayBGM(self, filenameWithoutExtension: str):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(f"assets/bgm/{filenameWithoutExtension}.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)    