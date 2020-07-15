import pygame
import os
from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT
from pygame import image, Rect, Surface, key, Vector2, transform, mask
from thefloatingdutchman.objects.object_sprite import ObjectSprite
from thefloatingdutchman.objects.bullets.bullet_data import BulletData

class BulletSprite(ObjectSprite):
    def __init__(self, bullet_data: BulletData):
        super().__init__(bullet_data)
        self.mask = mask.from_surface(self.image)
    
    def _set_original_image(self):
        sprite_sheet = image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Cannonball.png")).convert_alpha()

        # exact dimension of player sprite
        temp_rect = Rect((0, 0, 18, 18))
        self._original_image = pygame.Surface(temp_rect.size, pygame.SRCALPHA)
        # sets image to a portion of spritesheet (surface)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)

        # makes player appropriate size
        # self._original_image = transform.scale(self._original_image, (int(313/4), int(207/4)))
    
    def update(self):
        self._data.pos += (self._data.direction * self._data.vel)
        self.rect.center = self._data.pos

        if(self.rect.right > WINDOW_WIDTH or self.rect.bottom > WINDOW_HEIGHT or self.rect.left < 0 or self.rect.top < 0):
            self.kill()