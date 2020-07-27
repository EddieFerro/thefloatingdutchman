import math

from pygame import time, draw, display

from thefloatingdutchman.objects.weapons.bullets.bullet_sprite import BulletSprite
from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, RED
from thefloatingdutchman.objects.weapons.bullets.bullet_data import BulletData
from thefloatingdutchman.utility.resource_container import ResourceContainer


class ExplodeBullet(BulletSprite):
    def __init__(self, resource_container: ResourceContainer, bullet_data: BulletData):
        super().__init__(resource_container, bullet_data)

    def update(self, player, screen):
        t = time.get_ticks()
        if (t - self._ticks) > self._data.life_time:
            self._ticks = t
            distance = math.hypot((abs(self.rect.centerx) - abs(player.rect.centerx)),
                                  (abs(self.rect.centery) - abs(player.rect.centery)))
            if distance < 150:
                draw.circle(screen, RED, (self.rect.x, self.rect.y), 100, 100)
                display.flip()
                display.update()
                display.flip()
                display.update()
                display.flip()
                display.update()
                self.kill()

                player.take_damage(3)

            else:
                draw.circle(screen, RED, (self.rect.x, self.rect.y), 100, 100)
                display.flip()
                display.update()
                display.flip()
                display.update()
                display.flip()
                display.update()

                self.kill()

        else:
            print("moving")
            self._data.pos += (self._data.direction * self._data.vel)
            self.rect.center = self._data.pos

        if (self.rect.right > WINDOW_WIDTH or self.rect.bottom > WINDOW_HEIGHT or self.rect.left < 0 or self.rect.top < 0):
            draw.circle(screen, RED, (self.rect.x, self.rect.y), 100, 100)
            display.flip()
            display.update()
            display.flip()
            display.update()
            self.kill()
