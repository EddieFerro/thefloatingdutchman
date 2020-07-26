from pygame import Rect, mask, Surface, SRCALPHA, time

from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT
from thefloatingdutchman.objects.object_sprite import ObjectSprite
from thefloatingdutchman.objects.weapons.bullets.bullet_data import BulletData
from thefloatingdutchman.utility.resource_container import ResourceContainer


class BulletSprite(ObjectSprite):
    def __init__(self, resource_container: ResourceContainer, bullet_data: BulletData):
        super().__init__(resource_container, bullet_data)
        self.mask = mask.from_surface(self.image)
        self._ticks = time.get_ticks()

    def _set_original_image(self, resource_container: ResourceContainer):
        sprite_sheet = resource_container.resources['laser_shot_1']

        temp_rect = Rect((0, 0, 20, 20))
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)

    def update(self):
        self._data.pos += (self._data.direction * self._data.vel)
        self.rect.center = self._data.pos

        if (self.rect.right > WINDOW_WIDTH or self.rect.bottom > WINDOW_HEIGHT or self.rect.left < 0 or self.rect.top < 0):
            self.kill()
