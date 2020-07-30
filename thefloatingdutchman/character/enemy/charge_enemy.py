import math

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, time, SRCALPHA, Rect

from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.utility.resource_container import ResourceContainer


class ChargeEnemy(EnemySprite):

    def __init__(self, res_container: ResourceContainer, enemy_data: EnemyData):
        super().__init__(res_container, enemy_data)
        self._pausing = 0
        self._charging = 0
        self._start = time.get_ticks()
        self._pstart = time.get_ticks()

    def _set_original_image(self, res_container: ResourceContainer):
        sprite_sheet = res_container.resources['red_fighter']
        temp_rect = Rect((0, 0, 32, 32))
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(
            self._original_image, (int(32*2.5), int(32*2.5)))
        self._original_image = transform.rotate(self._original_image, -90)

    def update(self, player: PlayerSprite, enemies: Group, screen: Surface):
        if(self._data.health <= 0):
            self.kill()
            enemies.remove(self)
        try:

            for enemy in enemies:
                if sprite.collide_circle(self, enemy) and enemy != self:
                    distance = math.hypot(
                        (enemy.rect.x - self.rect.x), (enemy.rect.y - self.rect.y))

                    if (distance < 400):
                        target_direction = Vector2(
                            (self.rect.x - enemy.rect.x), (self.rect.y - enemy.rect.y))
                        target_direction.scale_to_length(
                            self._data.vel * 0.001)
                        self.rect.x += target_direction.x
                        self.rect.y += target_direction.y

                # Delete enemy when it comes into contact with player
            if sprite.collide_mask(player, self) is not None and not player.invulnerable:
                player.take_damage(1)
                self.kill()
                enemies.remove(self)

                # Type 2 enemy specification
                # Auto fire towards player at a given rate

            n = time.get_ticks()

            if (self._charging) <= 1000:
                self._charging = n - self._start
                self._pstart = time.get_ticks()
                target_direction = Vector2(
                    - self.rect.x + player.rect.x,
                    - self.rect.y + player.rect.y)
                target_direction.scale_to_length(self._data.vel*2)
                self.rect.x += target_direction.x
                self.rect.y += target_direction.y
            elif (self._charging > 1000):
                self._pausing = time.get_ticks() - self._pstart

            if(self._pausing) > 550:
                self._charging = 0
                self._pausing = 0
                self._start = time.get_ticks()

            screen_rect = screen.get_rect()

            self.rect.clamp_ip(screen_rect)

            self._data.pos = Vector2(self.rect.center)

            self._calc_rotation(player)

        except ValueError:
            return
