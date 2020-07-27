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

class FirstBoss(WeaponEnemy):

    def __init__(self, res_container, enemy_data):
        super().__init__(res_container, enemy_data)
        self.radius = 600
        self.health_bar = EnemyHealthBar(self._data.health, self.rect)
        self.dead = False
        self.temp_weapon = MultiShotWeapon(res_container)

    def _set_original_image(self, res_container: ResourceContainer):
        sprite_sheet = res_container.resources['minion_boss']
        temp_rect = Rect((0, 0, 512, 512))

        scale = 0.9
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(
            self._original_image, (int(512*scale), int(512*scale)))
        self._original_image = transform.rotate(self._original_image, -90) 
    
    def update(self, player: PlayerSprite, enemies: Group, screen: Surface):
        if self._data.health <= 0:
            self.dead = True
            self.kill()
        
        if sprite.collide_mask(player, self) is not None and not player.invulnerable:
            player.take_damage(2.5)
            self.take_damage(50)
        
        state = self._data.state
        if state is BossState.STATIONARY:
            target_direction = Vector2(0,0)
            self._data.attack_speed = 1500
            self._calc_rotation(player)
            self.image.set_alpha(255)
            self._data.vel = 5
            self._weapon.fire(player, self._data.attack_speed, 10, self.rect)
            self._weapon.update()

        elif state is BossState.TRANSITION:
            target_direction = Vector2(0,0)
            self._weapon = self.temp_weapon
            self._weapon.spawn()
            self._data.invulnerable = True
            self.image.set_alpha(100)
            self.invulnerable_start = time.get_ticks()

        elif state is BossState.ENRAGED:
            self._data.invulnerable = False
            target_direction = player._data.pos - self._data.pos
            target_direction = self._avoid_player(player, target_direction)
            self._data.attack_speed = 700
            self._calc_rotation(player)
            self.image.set_alpha(255)
            self._data.vel = 7
            self._weapon.fire(player, self._data.attack_speed, 20, self.rect, 5)
            self._weapon.update()

        if target_direction.length() != 0:
            target_direction.scale_to_length(self._data.vel)
        screen_rect = screen.get_rect()
        self._data.pos += target_direction
        self.rect = self.image.get_rect(center=self._data.pos)
        self.rect.clamp_ip(screen_rect)
            

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