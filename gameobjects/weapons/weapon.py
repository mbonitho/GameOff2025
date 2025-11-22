from pygame import Surface
from gameobjects.bullet import Bullet

class Weapon:
    def __init__(self, owner, weaponSurface: Surface, bulletSurface: Surface):     

        self.Owner = owner

        self.WeaponSurface = weaponSurface
        self.BulletSurface = bulletSurface
        self.Rect = self.WeaponSurface.get_rect()
        self.Rect.topleft = (0, 0)
        self.Bullets = []
        self.TotalBulletsShot = 0

        # customizable attributes for this weapon
        self.MaxBulletsOnScreen = 3
        self.BulletDamage = 1 # todo use
        self.TotalAmunition = -1
        self.BulletLifespan = 0 # todo use
        self.BulletSpeed = 0 # todo use
        self.BulletScale = 1 # todo use
        self.Angles = {
            'l': [180],
            'r': [0],
            'u': [270],
            'd': [90]
        }

    def update(self, enemies: list,  dt: float):
        for bullet in self.Bullets.copy():
            bullet.update(enemies, dt, self.Owner.playerIndex)
            if bullet.lifespan >= bullet.max_lifespan:
                self.Bullets.remove(bullet)

    def draw(self, screen):
        # screen.blit(self.WeaponSurface, self.Rect.topleft)
        for bullet in self.Bullets:
            bullet.draw(screen)

    def TryShootBullet(self, direction: str):

        if len(self.Bullets) >= self.MaxBulletsOnScreen * len(self.Angles['l']):
            return

        # substract any bullet shot, and reinit the player weapon when no more bullet
        if self.TotalAmunition != -1: 
            self.TotalBulletsShot += 1
            if self.TotalBulletsShot >= self.TotalAmunition:
                self.Owner.initializeWeapon()

        origin = (-1,-1)

        match direction:

            case 'l':
                origin = self.Owner.Rect.midleft

            case 'r':
                origin = self.Owner.Rect.midright

            case 'u':
                origin = self.Owner.Rect.midtop

            case 'd':
                origin = self.Owner.Rect.midbottom

        self.Rect.topleft = origin
        for angle in self.Angles[direction]:
            bullet = Bullet(self.BulletSurface, origin, angle)
            self.Bullets.append(bullet)
