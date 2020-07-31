from abc import ABC, abstractmethod

from pygame.sprite import Group

from thefloatingdutchman.utility.resource_container import ResourceContainer
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.objects.weapons.bullets.bullet_sprite import BulletSprite


class Weapon(Manager, ABC):
    def __init__(self, res_container: ResourceContainer, bullet_type=BulletSprite):
        super().__init__(res_container)
        self._bullet_type = bullet_type
        self._bullets = None
        self._prev_shot = 0
        self._first_shot = True

    def spawn(self):
        self._bullets = Group()

    def update(self, *args):
        self._bullets.update(*args)

    @abstractmethod
    def fire(self) -> bool:
        """Returns true if weapon fired"""
        pass

    def draw(self, screen):
        self._bullets.draw(screen)

    @property
    def prev_shot(self):
        return self._prev_shot
