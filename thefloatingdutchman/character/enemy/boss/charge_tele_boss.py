import random

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, time, Rect, SRCALPHA

from thefloatingdutchman.character.enemy.weapon_enemy import WeaponEnemy
from thefloatingdutchman.character.enemy.boss.boss_data import BossData, BossState
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.user_interface.enemy_health_bar import EnemyHealthBar
from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT
from thefloatingdutchman.utility.resource_container import ResourceContainer
from thefloatingdutchman.objects.weapons.multi_shot_weapon import MultiShotWeapon


class ChargeTeleBoss(WeaponEnemy):
    def __init__(self, res_container: ResourceContainer, boss_data: BossData):
        super().__init__(res_container, boss_data, MultiShotWeapon)
        self.radius = 600
        self.flash = True
        self.health_bar = EnemyHealthBar(self._data.health, self.rect)
        self.pausing = 0
        self.charging = 0
        self.start = time.get_ticks()
        self.pstart = time.get_ticks()
        self.moved = False

    def _set_original_image(self, res_container: ResourceContainer):
        sprite_sheet = res_container.resources['alien_boss_sprite']
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

        # self._bullets.update()
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

        if state is BossState.TELEPORT:
            self._weapon.fire(
                player, self._data.attack_speed, 15, self.rect, 4)
        else:
            self._weapon.fire(
                player, self._data.attack_speed, 15, self.rect, 2)

        self._weapon.update()

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
        screen.blit(self.image, self.rect)
