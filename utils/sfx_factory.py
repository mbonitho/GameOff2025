import pygame



class SFXFactory:

    _sounds = {}

    @classmethod
    def PlayElevatorDoorsOpenSFX(cls):
        return cls._playSFX('elevator_doors_open')

    @classmethod
    def PlayElevatorDoorsOpen2SFX(cls):
        return cls._playSFX('elevator_doors_open2')

    @classmethod
    def PlayElevatorMusicSFX(cls):
        return cls._playSFX('elevator_music')

    @classmethod
    def PlayElevatorFloorAnouncementSFX(cls, floorNumber: int):
        return cls._playSFX(f'elevator_F{floorNumber}')

    @classmethod
    def PlayBossDeath1SFX(cls):
        return cls._playSFX('boss_death_1')

    @classmethod
    def PlayBossDeath2SFX(cls):
        return cls._playSFX('boss_death_2')

    @classmethod
    def PlayBossDeath3SFX(cls):
        return cls._playSFX('boss_death_3')

    @classmethod
    def PlayBossDeath4SFX(cls):
        return cls._playSFX('boss_death_4')


    @classmethod
    def _playSFX(cls, filename: str):
        if filename not in cls._sounds:
            cls._sounds[filename] = pygame.mixer.Sound(f'assets/sfx/{filename}.wav')

        cls._sounds[filename].play()

        return cls._sounds[filename]