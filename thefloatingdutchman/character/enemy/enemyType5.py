import random

import math

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, Rect, SRCALPHA

from thefloatingdutchman.objects.weapons.bullets.explode_bullet import ExplodeBullet
from thefloatingdutchman.objects.weapons.enemy_weapon import EnemyWeapon
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.character.enemy.weapon_enemy import WeaponEnemy
from thefloatingdutchman.utility.resource_container import ResourceContainer


class EnemyType5(WeaponEnemy):

    def __init__(self, res_container: ResourceContainer, enemy_data: EnemyData):
        super().__init__(res_container, enemy_data)
        self._weapon = EnemyWeapon(res_container, ExplodeBullet)
        self._weapon.spawn()
        self._prev_shot = 0

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
            # Check for nearby enemies, only move in certain case
            for enemy in enemies:
                if sprite.collide_circle(self, enemy) and enemy != self:
                    distance = math.hypot(
                        (enemy.rect.x - self.rect.x), (enemy.rect.y - self.rect.y))

                    if (distance < 400):
                        target_direction = Vector2(
                            (self.rect.x - enemy.rect.x), (self.rect.y - enemy.rect.y))
                        target_direction.scale_to_length(
                            self._data.vel * 0.0001)
                        self.rect.x += target_direction.x
                        self.rect.y += target_direction.y

            # Type 2 enemy backs away from player
            distance = math.hypot(
                (player.rect.x - self.rect.x), (player.rect.y - self.rect.y))
            if (distance > 550):
                self._data._stopMoving = False

            # Enemy moves toward player given that they are either type 1 or sufficiently far enough from player
            if not self._data._stopMoving:
                target_direction = Vector2(
                    - self.rect.x + player.rect.x + random.randrange(0, 30), - self.rect.y + player.rect.y + random.randrange(0, 30))
                target_direction.scale_to_length(self._data.vel * 0.9)

            # Delete enemy when it comes into contact with player
            if sprite.collide_mask(player, self) is not None and not player.invulnerable:
                player.take_damage(1)
                self.kill()
                enemies.remove(self)

            self._weapon.fire(player, self._data.attack_speed,
                              15, self.rect, 550)
            self._weapon.update(player, screen)

            # Stop moving towards player at a certain distance
            if sprite.collide_circle(self, player):
                self._data._stopMoving = True
                distance = math.hypot(
                    (player.rect.x-self.rect.x), (player.rect.y - self.rect.y))
                # Move back if in danger zone
                if(distance < 550):
                    target_direction = Vector2(
                        (self.rect.x - player.rect.x), (self.rect.y - player.rect.y))
                    target_direction.scale_to_length(self._data.vel * 1.01)
                    self.rect.x += target_direction.x
                    self.rect.y += target_direction.y

            # All other cases are given movement data here
            if self._data._stopMoving is False:
                self.rect.x += target_direction.x
                self.rect.y += target_direction.y

            screen_rect = screen.get_rect()

            self.rect.clamp_ip(screen_rect)

            self._data.pos = Vector2(self.rect.center)

            self._calc_rotation(player)

        except ValueError:
            return
