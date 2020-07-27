import random
import math

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, time, Rect, SRCALPHA

from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from thefloatingdutchman.character.enemy.weapon_enemy import WeaponEnemy
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.utility.resource_container import ResourceContainer


class RangedTeleportEnemy(WeaponEnemy):

    def __init__(self, res_container: ResourceContainer, enemy_data: EnemyData):
        super().__init__(res_container, enemy_data)
        self._moved = True
        self._prev_shot = 0

    def _set_original_image(self, res_container: ResourceContainer):
        sprite_sheet = res_container.resources['red_fighter']
        temp_rect = Rect((0, 0, 32, 32))
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(
            self._original_image, (int(32 * 2.5), int(32 * 2.5)))
        self._original_image = transform.rotate(self._original_image, -90)

    def update(self, player: PlayerSprite, enemies: Group, screen: Surface):
        if (self._data.health <= 0):
            self.kill()
            enemies.remove(self)
        rand_pos_x = random.randint(40, WINDOW_WIDTH / 2)

        rand_pos_y = random.randint(40, WINDOW_HEIGHT / 2)

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

        n = time.get_ticks()
        if (n - self._prev_shot) > 2000 and not self._moved:
            self.rect.x = rand_pos_x
            self.rect.y = rand_pos_y
            # t = time.get_ticks()
            self._moved = True

        elif (n - self._prev_shot) > 3000 and self._moved:

            if self._weapon.fire(player, self._data.attack_speed, 15, self.rect):
                self._moved = False

        else:
            self.rect.x = self.rect.x
            self.rect.y = self.rect.y

        screen_rect = screen.get_rect()

        self.rect.clamp_ip(screen_rect)

        self._data.pos = Vector2(self.rect.center)

        self._calc_rotation(player)
        self._weapon.update()
