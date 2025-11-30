import random
import pygame



class SFXFactory:

    _sounds = {}

    @classmethod
    def PlaySplashSFX(cls):
        return cls._playSFX('misc_badabim_badaboom')

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
    def PlayUziSFX(cls):
        sound_name = random.choice(['gun_uzi_1', 'gun_uzi_2', 'gun_uzi_3'])
        return cls._playSFX(sound_name)
    
    @classmethod
    def PlayM9SFX(cls):
        sound_name = random.choice(['gun_m9_1', 'gun_m9_2', 'gun_m9_3'])
        return cls._playSFX(sound_name)
    
    @classmethod
    def PlayMusketSFX(cls):
        sound_name = random.choice(['gun_musket_1', 'gun_musket_2'])
        return cls._playSFX(sound_name)

    @classmethod
    def PlayBombExplodingSFX(cls):
        sound_name = random.choice(['item_bomb_1', 'item_bomb_2'])
        return cls._playSFX(sound_name)

    @classmethod
    def PlayMineExplodingSFX(cls):
        sound_name = random.choice(['item_mine_1', 'item_mine_2'])
        return cls._playSFX(sound_name)

    @classmethod
    def PlayShotGunSFX(cls):
        sound_name = random.choice(['gun_shotgun_1', 'gun_shotgun_2'])
        return cls._playSFX(sound_name)

    @classmethod
    def PlayFootstepsSFX(cls, playerindex: int):
        return cls._playSFX(f'player{playerindex}_steps', True)

    @classmethod
    def PlayPlayerHappySFX(cls, playerindex: int):
        return cls._playSFX(f'player{playerindex}_happy')

    @classmethod
    def PlayPlayerDrinksSFX(cls, playerindex: int):
        return cls._playSFX(f'player{playerindex}_drinks')

    @classmethod
    def PlayPlayerHealedSFX(cls, playerindex: int):
        return cls._playSFX(f'player{playerindex}_healed')

    @classmethod
    def PlayPlayerHurtSFX(cls, playerindex: int):
        return cls._playSFX(f'player{playerindex}_hurt{random.choice([1,2])}')

    @classmethod
    def PlayPlayerDeadSFX(cls, playerindex: int):
        return cls._playSFX(f'player{playerindex}_dead')

    @classmethod
    def PlayWeeeeeSFX(cls):
        return cls._playSFX('misc_weee')

    @classmethod
    def _playSFX(cls, filename: str, loop: bool = False):
        if filename not in cls._sounds:
            cls._sounds[filename] = pygame.mixer.Sound(f'assets/sfx/{filename}.wav')

        if loop:
            cls._sounds[filename].play(-1)
        else:
            cls._sounds[filename].play()

        return cls._sounds[filename]