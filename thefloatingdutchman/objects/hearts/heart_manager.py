import random

from pygame import Vector2, sprite, Surface

from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from .heart_data import HeartData
from .heart_sprite import HeartSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.character.character_sprite import CharacterSprite



class HeartManager(Manager):
    def __init__(self):
        super().__init__()

    def spawn(self, level: int):
        self._hearts = sprite.Group()
        self._add_hearts(level)


    def _add_hearts(self, level: int):
            # picking position a fair distance away from player
            rand_pos_x: int = random.randint(40, WINDOW_WIDTH/2 - 200) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_WIDTH/2 + 200, WINDOW_WIDTH - 40)

            rand_pos_y: int = random.randint(40, WINDOW_HEIGHT/2 - 100) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_HEIGHT/2 + 100, WINDOW_HEIGHT - 40)
            type2Chance = 0.2 + (level * 0.03)
            type1Chance = 1 - type2Chance
            spawnTwo = random.choices([True, False], weights=[type2Chance, type1Chance], k=1)[0]
            if not spawnTwo:
                self._hearts.add(
                    HeartSprite(
                        HeartData(
                            1500,
                            Vector2(rand_pos_x, rand_pos_y),
                            0,
                        )
                    ),
                    HeartSprite(
                        HeartData(
                            1500,
                            Vector2(rand_pos_x, rand_pos_y),
                            0,
                        )
                    )
                )
            else:
                self._hearts.add(
                    HeartSprite(
                        HeartData(
                            1500,
                            Vector2(rand_pos_x, rand_pos_y),
                            0,
                        )
                    )
                )

    def get_heart_count(self) -> int:
        return len(self._hearts.sprites())

    def update(self, player: PlayerSprite, screen: Surface, character: CharacterSprite):
        self._hearts.update(player, self._hearts, screen, character)

    def draw(self, screen: Surface):
        self._hearts.draw(screen)
