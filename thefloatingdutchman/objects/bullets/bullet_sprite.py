import os
import math
from pygame import image, Rect, mask, Surface, SRCALPHA, time, draw, display

from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, RED
from thefloatingdutchman.objects.object_sprite import ObjectSprite
from thefloatingdutchman.objects.bullets.bullet_data import BulletData


class BulletSprite(ObjectSprite):
    def __init__(self, bullet_data: BulletData):
        super().__init__(bullet_data)
        self.mask = mask.from_surface(self.image)
        self._ticks = time.get_ticks()

    def _set_original_image(self):
        sprite_sheet = image.load(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "Cannonball.png")).convert_alpha()

        # exact dimension of player sprite
        temp_rect = Rect((0, 0, 18, 18))
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        # sets image to a portion of spritesheet (surface)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)

        # makes player appropriate size
        # self._original_image = transform.scale(self._original_image, (int(313/4), int(207/4)))

    def update(self, player=None, screen=None):

        self._data.pos += (self._data.direction * self._data.vel)
        self.rect.center = self._data.pos
        t = time.get_ticks()
        if (t - self._ticks) > self._data.life_time and (self._data.type5):
            self._ticks = t

            if (player):
                distance = math.hypot(
                    (player.rect.x - self.rect.x), (player.rect.y - self.rect.y))
                if distance < 150:
                    player.take_damage(1)
                draw.circle(screen, RED, (self.rect.x, self.rect.y), 100, 100)
                display.update()
                self.kill()

            draw.circle(screen, RED, (self.rect.x, self.rect.y), 100, 100)
            display.update()
            self.kill()

        if (self.rect.right > WINDOW_WIDTH or self.rect.bottom > WINDOW_HEIGHT or self.rect.left < 0 or self.rect.top < 0):
            if(self._data.type5):
                draw.circle(screen, RED, (self.rect.x, self.rect.y), 100, 100)
                display.update()
            self.kill()
