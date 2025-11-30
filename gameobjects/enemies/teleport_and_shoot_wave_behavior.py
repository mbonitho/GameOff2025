import random
from typing import List
from pygame import Surface
from gameobjects.enemies.enemy_behavior import EnemyBehavior
from gameobjects.bullet import Bullet

class TeleportAndShootWaveBehavior(EnemyBehavior):

    def __init__(self, bullet_surface: Surface, angleRange: tuple[int, int]):
        super().__init__()

        self.BulletSurface = bullet_surface

        self.attack_timer = 0
        self.attack_cooldown = random.randrange(1,3) # seconds

        self.Bullets : List[Bullet] = []
        self.AngleRange: tuple[int, int] = angleRange


    def update(self, enemy, players, dt):
        
        self.attack_timer += dt
        if self.attack_timer >= self.attack_cooldown:
            self.attack_timer %= self.attack_cooldown

            # choose a random angle, and shoot
            angle = random.randrange(self.AngleRange[0], self.AngleRange[1])
            bullet = Bullet(self.BulletSurface, enemy.Rect.center, angle)
            bullet.max_lifespan = 10 # seconds
            bullet.Speed = 2 * 60 # way slower than bullets
            self.Bullets.append(bullet)

            # randomize shoot timing
            self.attack_cooldown = random.randrange(3, 10)  # seconds

        for bullet in self.Bullets.copy():
            bullet.update(players, dt)

            if bullet.lifespan >= bullet.max_lifespan:
                self.Bullets.remove(bullet)

    
    def draw(self, screen, enemy):
        for bullet in self.Bullets:
            bullet.draw(screen)