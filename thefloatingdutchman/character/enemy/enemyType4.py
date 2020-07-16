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
class EnemyType4(EnemySprite):

    def __init__(self,  enemy_data: EnemyData):
        super().__init__(enemy_data)
        self._pausing = 0
        self._charging = 0
        self._start = pygame.time.get_ticks()
        self._pstart = 0

    def _set_original_image(self):
        sprite_sheet = image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Red Fighter.png")).convert_alpha()
        temp_rect = Rect((0,0,32,32))
        self._original_image = pygame.Surface(temp_rect.size, pygame.SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(self._original_image, (int(32*2.5), int(32*2.5)))
        self._original_image = transform.rotate(self._original_image, -90)

    def update(self, player: PlayerSprite, enemies: Group, screen: Surface):
        if(self._data.health <= 0):
            self.kill()
        try:

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
                # Update bullets
                self._bullets.update()

                # Delete enemy when it comes into contact with player
                if sprite.collide_mask(player, self) is not None:
                    player.take_damage(5)
                    enemies.remove(self)

                # Type 2 enemy specification
                    # Auto fire towards player at a given rate


                n = pygame.time.get_ticks()

                if (self._charging) < 500:
                    self._charging = n - self._start
                    self._pstart = pygame.time.get_ticks()
                    print(self._charging)
                    target_direction = Vector2(
                        - self.rect.x + player.rect.x + random.randrange(0, 30),
                        - self.rect.y + player.rect.y + random.randrange(0, 30))
                    target_direction.scale_to_length(self._data.vel * 2)
                    self.rect.x += target_direction.x
                    self.rect.y += target_direction.y
                elif (self._charging > 500):
                    self.rect.x += 0
                    self.rect.y += 0
                    self._pausing= pygame.time.get_ticks() - self._pstart



                if(self._pausing) > 1000:
                    self._start = pygame.time.get_ticks()
                    self._charging =0
                    self._pausing=0


                screen_rect = screen.get_rect()

                self.rect.clamp_ip(screen_rect)

                self._data.pos = Vector2(self.rect.center)

                self._calc_rotation(player)







        except ValueError:
            return
