import random

from pygame import Vector2, sprite, Surface

from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from .hearts.heart_data import HeartData
from .hearts.heart_sprite import HeartSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.character.character_sprite import CharacterSprite


class DropManager(Manager):
    def __init__(self):
        super().__init__()
        self._hearts = None

    # Initialize all new sprite groups and call
    def spawn(self, level: int):
        self._hearts = sprite.Group()

    def update(self, player: PlayerSprite, screen: Surface, character: CharacterSprite):
        self._heart_update(player, screen, character)

    # Add drop functions for new items to the drop method

    def drop_items(self, level: int):
        self._drop_hearts(self, level)

    def _drop_hearts(self, level: int):
        self._hearts = sprite.Group()
        x = range(2)
        for i in x:
            # picking position a fair distance away from player
            rand_pos_x: int = random.randint(40, WINDOW_WIDTH / 2 - 200) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_WIDTH / 2 + 200, WINDOW_WIDTH - 40)

            rand_pos_y: int = random.randint(40, WINDOW_HEIGHT / 2 - 100) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_HEIGHT / 2 + 100, WINDOW_HEIGHT - 40)
            self._hearts.add(
                HeartSprite(
                    HeartData(
                        1500,
                        Vector2(rand_pos_x, rand_pos_y),
                        0,
                    )
                )
            )
            self._draw_hearts()

    def _heart_update(self, player: PlayerSprite, screen: Surface, character: CharacterSprite):
        self._hearts.update(player, self._hearts, screen, character)
        hits = sprite.spritecollide(
            player, self._hearts, True, sprite.collide_mask)
        for pickups in hits:
            character.gain_health(20)

    def _get_heart_count(self) -> int:
        return len(self._hearts.sprites())

    def _draw_hearts(self, screen: Surface):
        self._hearts.draw(screen)
