import math

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface

import pygame
from objects.bullets.bullet_data import BulletData
from objects.bullets.bullet_sprite import BulletSprite

from character.character_sprite import CharacterSprite
from character.player.player_sprite import PlayerSprite
from character.enemy.enemy_data import EnemyData
from game_settings import GREEN


class EnemySprite(CharacterSprite):
    def __init__(self, enemy_data: EnemyData):
        super().__init__(enemy_data)
        self._prev_shot = 0
        self._bullets = sprite.Group()
        self._angle = 0


        self.radius = 50

    def _set_original_image(self):
        self._original_image = Surface((20, 50))
        self._original_image.fill(GREEN)

    # Enemy AI might go in here
    def update(self, player: PlayerSprite, enemies: Group):
        direction_vector = Vector2(
            - self.rect.x + player.rect.x, - self.rect.y + player.rect.y)
        try:
            direction_vector.scale_to_length(self._data.vel)
            if self.rect.colliderect(player.rect):
                enemies.remove(self)


            for enemy in enemies:
                if pygame.sprite.collide_circle(self, enemy) and enemy != self:
                    direction_vector = Vector2(
                        (self.rect.x - enemy.rect.x),  (self.rect.y - enemy.rect.y))
                    direction_vector.scale_to_length(self._data.vel*2)
            if self._data._type2:
                t = pygame.time.get_ticks()
                if (t - self._prev_shot) > 10:
                    self._prev_shot = t
                    self._angle = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
                    self._angle = math.degrees(self._angle)
                    direction = Vector2(
                        1, 0).rotate(self._angle)
                    BulletSprite(BulletData(10, direction, 0, Vector2(self.rect.x, self.rect.y), 50)).add(self._bullets)
                    self._bullets.update()
                if pygame.sprite.collide_circle(self, player):
                    direction_vector = Vector2(
                        (self.rect.x - player.rect.x),  (self.rect.y - player.rect.y))
                    direction_vector.scale_to_length(self._data.vel*2)
            self.rect.x += direction_vector.x
            self.rect.y += direction_vector.y


        except ValueError:
            return
