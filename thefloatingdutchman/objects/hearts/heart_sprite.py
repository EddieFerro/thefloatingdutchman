from pygame.sprite import Group

from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT
from pygame import Rect, Surface, transform, mask, SRCALPHA
from thefloatingdutchman.objects.object_sprite import ObjectSprite
from .heart_data import HeartData
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.utility.resource_container import ResourceContainer


class HeartSprite(ObjectSprite):
    def __init__(self, resource_container: ResourceContainer, heart_data: HeartData):
        super().__init__(resource_container, heart_data)
        self.mask = mask.from_surface(self.image)

    def _set_original_image(self, resource_container: ResourceContainer):
        sprite_sheet = resource_container.resources['heart']
        temp_rect = Rect((0, 0, 254, 254))
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(
            self._original_image, (int(70), int(70)))

    def update(self, hearts: Group, player: PlayerSprite, screen: Surface):
        self.rect.center = self._data.pos
        if (self.rect.right > WINDOW_WIDTH or self.rect.bottom > WINDOW_HEIGHT or self.rect.left < 0 or self.rect.top < 0):
            self.kill()
