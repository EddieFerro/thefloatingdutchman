import random
import math

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, Rect, SRCALPHA

from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.utility.resource_container import ResourceContainer


class ChaseEnemy(EnemySprite):

    def __init__(self, res_container: ResourceContainer, enemy_data: EnemyData):
        super().__init__(res_container, enemy_data)

    def _set_original_image(self, res_container: ResourceContainer):
        sprite_sheet = res_container.resources['green_fighter']
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

        for enemy in enemies:
            # Check for nearby enemies to avoid collision
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

        target_direction = Vector2(
            - self.rect.x + player.rect.x + random.randrange(0, 30),
            - self.rect.y + player.rect.y + random.randrange(0, 30))
        target_direction.scale_to_length(self._data.vel * 0.7)

        # Delete enemy when it comes into contact with player
        if sprite.collide_mask(player, self) is not None and not player.invulnerable:
            player.take_damage(1)
            self.kill()
            enemies.remove(self)

        self.rect.x += target_direction.x
        self.rect.y += target_direction.y

        screen_rect = screen.get_rect()

        self.rect.clamp_ip(screen_rect)

        self._data.pos = Vector2(self.rect.center)

        self._calc_rotation(player)
