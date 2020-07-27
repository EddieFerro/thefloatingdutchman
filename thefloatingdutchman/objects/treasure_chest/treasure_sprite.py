from pygame import Rect, Surface, transform, mask, SRCALPHA

from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT
from thefloatingdutchman.objects.object_sprite import ObjectSprite
from thefloatingdutchman.objects.treasure_chest.treasure_data import TreasureData
from thefloatingdutchman.utility.resource_container import ResourceContainer


class TreasureSprite(ObjectSprite):
    def __init__(self, resource_container: ResourceContainer, treasure_data: TreasureData):
        super().__init__(resource_container, treasure_data)
        self.mask = mask.from_surface(self.image)

    def _set_original_image(self, resource_container: ResourceContainer):
        sprite_sheet = resource_container.resources['treasure']
        temp_rect = Rect((0, 0, 254, 254))
        scale = 0.3
        self._original_image = Surface(temp_rect.size, SRCALPHA)

        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(
            self._original_image, (int(254*scale), int(254*scale)))

    def update(self):
        self.rect.center = self._data.pos
        if (self.rect.right > WINDOW_WIDTH or self.rect.bottom > WINDOW_HEIGHT or self.rect.left < 0 or self.rect.top < 0):
            self.kill()
