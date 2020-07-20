import random
import math
import os

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, time, Rect, image, SRCALPHA

from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.character.enemy.boss.boss_data import BossData
from thefloatingdutchman.objects.bullets.bullet_data import BulletData
from thefloatingdutchman.objects.bullets.bullet_sprite import BulletSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite


class MinionBoss(EnemySprite):
    def __init__(self, boss_data: BossData):
        super().__init__(boss_data)
        self.radius = 600
        self._return_mode = False
        self._start_pos = None
        self.invulnerable = False
        self.invulnerable_start = 0
        self.flash = True

    def _set_original_image(self):
        sprite_sheet = image.load(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "minion_boss.png")).convert_alpha()
        temp_rect = Rect((0, 0, 512, 512))

        scale = 0.9
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(
            self._original_image, (int(512*scale), int(512*scale)))
        self._original_image = transform.rotate(self._original_image, -90)

    def update(self, player: PlayerSprite, enemies: Group, screen: Surface) -> None:

        if(self._data.health <= 0):
            self.kill()

        self._prevent_enemy_collision(enemies)

        # Ranged enemies back away from player
        dist_from_player = self._data.pos.distance_to(player._data.pos)
        if (dist_from_player > 400):
            self._data._stopMoving = False

        self._bullets.update()

        # Delete enemy when it comes into contact with player
        if sprite.collide_mask(player, self) is not None and not player.invulnerable:
            player.take_damage(3)
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
            BulletSprite(BulletData(direction, 0, Vector2(self._data.pos), 25)).add(
                self._bullets)

        # ranged enemies avoid the player
        if not self._return_mode:
            self._avoid_player(player)

        if not self._data._stopMoving and not self._return_mode:
            target_direction = player._data.pos - self._data.pos
            target_direction.scale_to_length(self._data.vel)
            self._data.pos += target_direction
            self.rect = self.image.get_rect(center=self._data.pos)
        elif self._return_mode:
            target_direction = self._data._initial_spawn - self._data.pos
            target_direction.scale_to_length(self._data.vel)
            self._data.pos += target_direction
            self.rect = self.image.get_rect(center=self._data.pos)

        screen_rect = screen.get_rect()
        self.rect.clamp_ip(screen_rect)
        self._data.pos = Vector2(self.rect.center)

        if self._return_mode:
            self._spin()
        else:
            self._calc_rotation(player)

    def _spin(self):
        self._angle += 10
        self._angle = self._angle % 360
        self.image = transform.rotate(self._original_image, self._angle)
        self.rect = self.image.get_rect(center=self._data.pos)

    def _prevent_enemy_collision(self, enemies: Group):
        # Check for nearby enemies, only move in certain case
        for enemy in enemies:
            if sprite.collide_circle(self, enemy) and enemy != self:
                dist_from_enemy = enemy._data.pos.distance_to(self._data.pos)

                if (dist_from_enemy < 600):
                    target_direction = self._data.pos - enemy._data.pos
                    target_direction.normalize()
                    target_direction.scale_to_length(self._data.vel * 0.0001)
                    self._data.pos += target_direction
                    self.rect = self.image.get_rect(center=self._data.pos)

    def _avoid_player(self, player: PlayerSprite):
        # Stop moving towards player at a certain distance
        if sprite.collide_circle(self, player):
            self._data._stopMoving = True
            distance = math.hypot(
                (player.rect.x-self.rect.x), (player.rect.y - self.rect.y))
            # Move back if in danger zone
            if(distance < 800):
                target_direction = self._data.pos - player._data.pos
                target_direction.normalize()
                target_direction.scale_to_length(self._data.vel)
                self._data.pos += target_direction
                self.rect = self.image.get_rect(center=self._data.pos)

    def take_damage(self, damage):
        if not self._return_mode:
            super().take_damage(damage)

    def draw(self, screen):
        if not self._return_mode:
            screen.blit(self.image, self.rect)
        else:
            if self.flash:
                screen.blit(self.image, self.rect)
            now = time.get_ticks()
            dt = now - self.invulnerable_start
            if dt % 500:
                self.flash = not self.flash
