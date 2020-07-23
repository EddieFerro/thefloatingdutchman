from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
import random
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
import math
import os
from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, Rect, image, mask

import pygame
from thefloatingdutchman.objects.bullets.bullet_data import BulletData
from thefloatingdutchman.objects.bullets.bullet_sprite import BulletSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH

from thefloatingdutchman.character.character_sprite import CharacterSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.game_settings import GREEN, RED


class EnemyType3(EnemySprite):

    def __init__(self, enemy_data: EnemyData):
        super().__init__(enemy_data)
        self._moved = True
        self._prev_shot = 0

    def _set_original_image(self):
        sprite_sheet = image.load(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "Red Fighter.png")).convert_alpha()
        temp_rect = Rect((0, 0, 32, 32))
        self._original_image = pygame.Surface(temp_rect.size, pygame.SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(self._original_image, (int(32 * 2.5), int(32 * 2.5)))
        self._original_image = transform.rotate(self._original_image, -90)

    def update(self, player: PlayerSprite, enemies: Group, screen: Surface):
        if (self._data.health <= 0):
            self.kill()
            enemies.remove(self)
        rand_pos_x = random.randint(40, WINDOW_WIDTH / 2)

        rand_pos_y = random.randint(40, WINDOW_HEIGHT / 2)

        try:
            # Update bullets
            self._bullets.update()
            for enemy in enemies:
                if pygame.sprite.collide_circle(self, enemy) and enemy != self:
                    distance = math.hypot((enemy.rect.x - self.rect.x), (enemy.rect.y - self.rect.y))
                    # print(distance)
                    if (distance < 400):
                        target_direction = Vector2(
                            (self.rect.x - enemy.rect.x), (self.rect.y - enemy.rect.y))
                        target_direction.scale_to_length(self._data.vel * 0.0001)
                        self.rect.x += target_direction.x
                        self.rect.y += target_direction.y
            # Delete enemy when it comes into contact with player
            if sprite.collide_mask(player, self) is not None and not player.invulnerable:
                player.take_damage(1)
                self.kill()
                enemies.remove(self)

            n = pygame.time.get_ticks()
            if (n - self._prev_shot) > 2000 and self._moved == False:
                self.rect.x = rand_pos_x
                self.rect.y = rand_pos_y
                t = pygame.time.get_ticks()
                self._moved = True

            elif (n - self._prev_shot) > 3000 and self._moved == True:
                t = pygame.time.get_ticks()
                if (t - self._prev_shot) > (self._data.attack_speed-1):
                    self._prev_shot = t
                    temp_angle = math.atan2(player.rect.centery - self.rect.centery,
                                            player.rect.centerx - self.rect.centerx)
                    temp_angle = math.degrees(temp_angle)
                    temp_angle += random.uniform(-15, 15)

                    direction = Vector2(1, 0).rotate(temp_angle)
                    BulletSprite(BulletData(direction, 0, ((self.rect.centerx, self.rect.centery)), 25, self.bullet_sprite)).add(self._bullets)
                    self._moved = False

            else:
                self.rect.x = self.rect.x
                self.rect.y = self.rect.y




            screen_rect = screen.get_rect()

            self.rect.clamp_ip(screen_rect)

            self._data.pos = Vector2(self.rect.center)

            self._calc_rotation(player)







        except ValueError:
            return
