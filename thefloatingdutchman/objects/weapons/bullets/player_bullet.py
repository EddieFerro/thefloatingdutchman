from pygame import Rect, Surface, SRCALPHA

from thefloatingdutchman.objects.weapons.bullets.bullet_sprite import BulletSprite
from thefloatingdutchman.objects.weapons.bullets.bullet_data import BulletData
from thefloatingdutchman.utility.resource_container import ResourceContainer


class PlayerBullet(BulletSprite):
    def __init__(self, resource_container: ResourceContainer, bullet_data: BulletData):
        super().__init__(resource_container, bullet_data)

    def _set_original_image(self, resource_container: ResourceContainer):
        sprite_sheet = resource_container.resources['cannonball']

        temp_rect = Rect((0, 0, 20, 20))
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
