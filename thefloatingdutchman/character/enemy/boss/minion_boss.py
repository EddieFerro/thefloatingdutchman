import random
import math
import os

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, time, Rect, image, SRCALPHA

from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.objects.bullets.bullet_data import BulletData
from thefloatingdutchman.objects.bullets.bullet_sprite import BulletSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite


class MinionBoss(EnemySprite):
    def __init__(self):
        super().__init__()

    def _set_original_image(self):
        sprite_sheet = image.load(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "minion_boss.png")).convert_alpha()
        temp_rect = Rect((0, 0, 32, 32))
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(
            self._original_image, (int(32*2.5), int(32*2.5)))
        self._original_image = transform.rotate(self._original_image, -90)

    def update(self, player: PlayerSprite, enemies: Group, screen: Surface) -> None:

        if(self._data.health <= 0):
            self.kill()

        self._prevent_enemy_collision(enemies)

        # Ranged enemies back away from player
        dist_from_player = math.hypot(
            (player.rect.x - self.rect.x), (player.rect.y - self.rect.y))

        if (dist_from_player > 300):
            self._data._stopMoving = False

        # Move towards player when far enough away
        if not self._data._stopMoving:
            target_direction = Vector2(
                - self.rect.x + player.rect.x + random.randrange(0, 30), - self.rect.y + player.rect.y + random.randrange(0, 30))
            target_direction.scale_to_length(self._data.vel * 0.9)

        self._bullets.update()

        # Delete enemy when it comes into contact with player
        if sprite.collide_mask(player, self) is not None:
            player.take_damage(30)
            enemies.remove(self)

        # Auto fire towards player at a given rate
        t = time.get_ticks()
        if (t - self._prev_shot) > self._data.attack_speed:
            self._prev_shot = t
            temp_angle = math.atan2(
                player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)
            temp_angle = math.degrees(temp_angle)
            temp_angle += random.uniform(-15, 15)
            direction = Vector2(1, 0).rotate(temp_angle)
            BulletSprite(BulletData(direction, 0, self._data.pos, 25)).add(
                self._bullets)

        # ranged enemies avoid the player
        self._avoid_player(player)

        if not self._data._stopMoving:
            self.rect.x += target_direction.x
            self.rect.y += target_direction.y

        screen_rect = screen.get_rect()

        self.rect.clamp_ip(screen_rect)

        self._data.pos = Vector2(self.rect.center)
        self._calc_rotation(player)

    def _prevent_enemy_collision(self, enemies: Group):
        # Check for nearby enemies, only move in certain case
        for enemy in enemies:
            if sprite.collide_circle(self, enemy) and enemy != self:
                dist_from_enemy = math.hypot(
                    (enemy.rect.x - self.rect.x), (enemy.rect.y - self.rect.y))

                if (dist_from_enemy < 400):
                    target_direction = Vector2(
                        (self.rect.x - enemy.rect.x), (self.rect.y - enemy.rect.y))
                    target_direction.scale_to_length(
                        self._data.vel * 0.0001)
                    self.rect.x += target_direction.x
                    self.rect.y += target_direction.y

    def _avoid_player(self, player: PlayerSprite):
        # Stop moving towards player at a certain distance
        if sprite.collide_circle(self, player):
            self._data._stopMoving = True
            distance = math.hypot(
                (player.rect.x-self.rect.x), (player.rect.y - self.rect.y))
            # Move back if in danger zone
            if(distance < 300):
                target_direction = Vector2(
                    (self.rect.x - player.rect.x), (self.rect.y - player.rect.y))
                target_direction.scale_to_length(self._data.vel * 1.01)
                self.rect.x += target_direction.x
                self.rect.y += target_direction.y
