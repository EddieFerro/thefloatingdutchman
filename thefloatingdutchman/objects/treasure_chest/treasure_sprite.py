
import pygame
import os
from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT
from pygame import image, Rect, Surface, key, Vector2, transform, mask, sprite
from thefloatingdutchman.objects.object_sprite import ObjectSprite
from .treasure_data import TreasureData
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.character_sprite import CharacterSprite
from pygame.sprite import Group


class TreasureSprite(ObjectSprite):
    def __init__(self, treasure_data: TreasureData):
        super().__init__(treasure_data)
        self.mask = mask.from_surface(self.image)

    def _set_original_image(self):
        sprite_sheet = image.load(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "treasure.png")).convert_alpha()
        temp_rect = Rect((0, 0, 254, 254))
        scale = 0.3

        self._original_image = pygame.Surface(temp_rect.size, pygame.SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(
            self._original_image, (int(254*scale), int(254*scale)))

    def update(self):
        self.rect.center = self._data.pos
        if (self.rect.right > WINDOW_WIDTH or self.rect.bottom > WINDOW_HEIGHT or self.rect.left < 0 or self.rect.top < 0):
            self.kill()