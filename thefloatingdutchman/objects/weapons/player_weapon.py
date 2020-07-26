from pygame import Rect, Vector2, time

from thefloatingdutchman.utility.resource_container import ResourceContainer
from thefloatingdutchman.objects.weapons.weapon import Weapon
from thefloatingdutchman.objects.weapons.bullets.player_bullet import PlayerBullet

from thefloatingdutchman.objects.weapons.bullets.bullet_sprite import BulletSprite
from thefloatingdutchman.objects.weapons.bullets.bullet_data import BulletData


class PlayerWeapon(Weapon):
    def __init__(self, res_container: ResourceContainer, bullet_type=PlayerBullet):
        super().__init__(res_container, bullet_type)

    def fire(self, angle: int, attack_speed: int, rect: Rect) -> bool:
        """Returns true if weapon fired"""
        t = time.get_ticks()
        if (t - self._prev_shot) > attack_speed:
            self._prev_shot = t
            direction = Vector2(1, 0).rotate(-angle)

            self._bullets.add(self._bullet_type(
                self._res_container, BulletData(direction, 0, Vector2(rect.center), 25)))
