import random
import math
import os

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, time, Rect, image, SRCALPHA

from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.character.enemy.boss.boss_data import BossData, BossState
from thefloatingdutchman.objects.bullets.bullet_data import BulletData
from thefloatingdutchman.objects.bullets.bullet_sprite import BulletSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.user_interface.enemy_health_bar import EnemyHealthBar
from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS


class ChargeTeleBoss(EnemySprite):
    def __init__(self, boss_data: BossData):
        super().__init__(boss_data)
        self.radius = 600
        self.flash = True
        self.health_bar = EnemyHealthBar(self._data.health, self.rect)
        self.pausing = 0
        self.charging = 0
        self.start = time.get_ticks()
        self.pstart = time.get_ticks()
        self.moved = False

    def _set_original_image(self):
        sprite_sheet = image.load(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "aliensprite.png")).convert_alpha()
        temp_rect = Rect((0, 0, 172, 302))

        scale = 0.9
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(
            self._original_image, (int(172*scale), int(302*scale)))
        self._original_image = transform.rotate(self._original_image, -90)

    def update(self, player: PlayerSprite, enemies: Group, screen: Surface) -> None:

        if self._data.health <= 0:
            self.kill()

        self._bullets.update()
        rand_pos_x = random.randint(player._data.pos.x+50, WINDOW_WIDTH)
        rand_pos_y = random.randint(player._data.pos.y+50, WINDOW_HEIGHT)

        # Delete enemy when it comes into contact with player
        if sprite.collide_mask(player, self) is not None and not player.invulnerable:
            player.take_damage(1)
            self._data.health -= 30

        state = self._data.state
        if state is BossState.CHARGE:
            target_direction = player._data.pos - self._data.pos
            if target_direction != 0:
                target_direction.scale_to_length(self._data.vel * 3)
            self._data.vel = 5
            self._data.attack_speed = 150
            self._calc_rotation(player)
            self._data.pos += target_direction



        elif state is BossState.STATIONARY:
            target_direction = Vector2(0, 0)
            self._data.attack_speed = 15000
            self._calc_rotation(player)
            self._data.pos += target_direction



        elif state is BossState.TELEPORT:
            self._data.attack_speed = 0
            self._data.vel = 5
            self._calc_rotation(player)
            self._data.pos.x = rand_pos_x
            self._data.pos.y = rand_pos_y


        screen_rect = screen.get_rect()


        self.rect = self.image.get_rect(center=self._data.pos)
        self.rect.clamp_ip(screen_rect)

        # Auto fire towards player at a given rate
        t = time.get_ticks()
        if (t - self._prev_shot) > self._data.attack_speed:
            self._prev_shot = t
            temp_angle = math.atan2(
                player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)
            orig_temp_angle = math.degrees(temp_angle)
            temp_angle = orig_temp_angle+random.uniform(-15, 15)
            direction = Vector2(1, 0).rotate(temp_angle)
            BulletSprite(BulletData(direction, 0, Vector2(self._data.pos), 25, self.bullet_sprite)).add(
                self._bullets)
            temp_angle = orig_temp_angle+random.uniform(-15, 15)
            direction = Vector2(1, 0).rotate(temp_angle)
            BulletSprite(BulletData(direction, 0, Vector2(self._data.pos), 25, self.bullet_sprite)).add(
                self._bullets)
            if(BossState.TELEPORT):
                temp_angle = orig_temp_angle + random.uniform(-15, 15)
                direction = Vector2(1, 0).rotate(temp_angle)
                BulletSprite(BulletData(direction, 0, Vector2(self._data.pos), 25, self.bullet_sprite)).add(
                    self._bullets)
                temp_angle = orig_temp_angle + random.uniform(-15, 15)
                direction = Vector2(1, 0).rotate(temp_angle)
                BulletSprite(BulletData(direction, 0, Vector2(self._data.pos), 25, self.bullet_sprite)).add(
                    self._bullets)




    def _avoid_player(self, player: PlayerSprite, target_direction: Vector2):
        # Stop moving towards player at a certain distance
        if sprite.collide_circle(self, player):
            distance = self._data.pos.distance_to(player._data.pos)

            # Move back if in danger zone
            if distance < self.radius - 100:
                return self._data.pos - player._data.pos
            else:
                return Vector2(0, 0)
        else:
            return target_direction

    def take_damage(self, damage):
        super().take_damage(damage)

    def draw(self, screen):
        self.health_bar.draw(screen, self._data.pos, self._data.health)
        # if self._data.state is BossState.ROAM or self._data.state is BossState.STATIONARY:
        screen.blit(self.image, self.rect)
        # elif self._data.state is BossState.RETURN:
        #     if self.flash:
        #         screen.blit(self.image, self.rect)

        #     self.flash = not self.flash
