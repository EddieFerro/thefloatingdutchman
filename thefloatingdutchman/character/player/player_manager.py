from pygame import Vector2, sprite, display, draw

from thefloatingdutchman.character.player.player_data import PlayerData
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.weapon_enemy import WeaponEnemy
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.game_settings import RED
from thefloatingdutchman.utility.resource_container import ResourceContainer


class PlayerManager(Manager):
    def __init__(self, res_container: ResourceContainer):
        super().__init__(res_container)
        self._player = None

    def spawn(self):
        player_data = PlayerData(4, 750, Vector2(
            display.Info().current_w/2, display.Info().current_h/2), 10)
        self._player = PlayerSprite(self._res_container, player_data)

    def draw(self, screen):
        self._player.draw(screen)

    def update(self, screen, enemies: sprite.Group(), newRoom):
        self._player.update(screen, newRoom)
        if enemies is not None:
            for enemy in enemies:
                if isinstance(enemy, WeaponEnemy):
                    hits = sprite.spritecollide(
                        self._player, enemy._weapon._bullets, True, lambda sp1, sp2: not sp1.invulnerable and sprite.collide_mask(sp1, sp2))
                    for bullet in hits:
                        if bullet._data.type5:
                            draw.circle(screen, RED, (bullet.rect.x,
                                                      bullet.rect.y), 100, 100)
                            display.flip()
                            display.update()
                            display.flip()
                            display.update()
                        self._player.take_damage(enemy._damage)
                        bullet.kill()

    @property
    def player(self):
        return self._player
