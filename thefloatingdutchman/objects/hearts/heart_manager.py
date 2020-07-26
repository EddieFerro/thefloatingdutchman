import random

from pygame import Vector2, sprite, Surface

from .heart_data import HeartData
from .heart_sprite import HeartSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.utility.resource_container import ResourceContainer


class HeartManager(Manager):
    def __init__(self, res_container: ResourceContainer):
        super().__init__(res_container)
        self._hearts = None

    def spawn(self, level: int):
        self._hearts = sprite.Group()
        self._add_hearts(level)

    def _add_hearts(self, level: int):
        x = range(2)
        for i in x:
            # picking position a fair distance away from player
            rand_pos_x: int = random.randint(40, WINDOW_WIDTH/2 - 200) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_WIDTH/2 + 200, WINDOW_WIDTH - 40)

            rand_pos_y: int = random.randint(40, WINDOW_HEIGHT/2 - 100) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_HEIGHT/2 + 100, WINDOW_HEIGHT - 40)
            self._hearts.add(
                HeartSprite(
                    self._res_container,
                    HeartData(
                        Vector2(rand_pos_x, rand_pos_y),
                        0,
                    )
                )
            )

    def get_heart_count(self) -> int:
        return len(self._hearts.sprites())

    def update(self, player: PlayerSprite, screen: Surface):
        self._hearts.update(player, self._hearts, screen)
        if player._data.health < player._data._max_health:
            hits = sprite.spritecollide(
                player, self._hearts, True, sprite.collide_mask)
            for pickups in hits:
                player._data.gain_health(1)

    def draw(self, screen: Surface):
        self._hearts.draw(screen)
