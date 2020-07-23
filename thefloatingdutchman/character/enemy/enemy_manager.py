import random

from pygame import Vector2, sprite, Surface

from thefloatingdutchman.character.enemy.chase_enemy import ChaseEnemy
from thefloatingdutchman.character.enemy.ranged_enemy import RangedEnemy
from thefloatingdutchman.character.enemy.ranged_teleport_enemy import RangedTeleportEnemy
from thefloatingdutchman.character.enemy.charge_enemy import ChargeEnemy
from thefloatingdutchman.character.enemy.enemyType5 import EnemyType5
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from thefloatingdutchman.manager import Manager


class EnemyManager(Manager):
    def __init__(self):
        super().__init__()
        self._enemies = None

    def spawn(self, level: int):
        self._enemies = sprite.Group()
        self._add_enemies(level)

    def _add_enemies(self, level: int):

        for i in range(random.randint(2, 4) + level):

            # picking position a fair distance away from center of screen (player spawn)
            rand_pos_x: int = random.randint(40, WINDOW_WIDTH/2 - 200) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_WIDTH/2 + 200, WINDOW_WIDTH - 40)

            rand_pos_y: int = random.randint(40, WINDOW_HEIGHT/2 - 100) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_HEIGHT/2 + 100, WINDOW_HEIGHT - 40)
            type2Chance = 0.1 + (level * 0.01)
            type1Chance = 0.25
            type3Chance = 0
            type4Chance = 0
            type5Chance = 0

            if(level+1) >= 2:
                type3Chance = 0.1 + (level * 0.03)
                type4Chance = 0.25
            if(level+1) >= 3:
                type5Chance = type2Chance
                type2Chance = type2Chance - 0.01

            enemyChooser = random.choices([1, 2, 3, 4, 5], weights=[
                                          type2Chance, type1Chance, type4Chance, type3Chance, type5Chance], k=1)[0]

            if enemyChooser == 2:

                self._enemies.add(
                    ChaseEnemy(
                        EnemyData(
                            random.randint(30, 50) + (level*5),
                            # random.randint(5, 15) + random.randint(0, level*2),
                            1500,
                            Vector2(rand_pos_x, rand_pos_y),
                            5
                        )
                    )
                )
            elif enemyChooser == 1:
                self._enemies.add(
                    RangedEnemy(
                        EnemyData(
                            random.randint(30, 50) + (level*5),
                            # random.randint(5, 15) + random.randint(0, level*2),
                            1500,
                            Vector2(rand_pos_x, rand_pos_y),
                            5
                        )
                    )
                )
            elif enemyChooser == 4:
                self._enemies.add(
                    RangedTeleportEnemy(
                        EnemyData(
                            random.randint(30, 50) + (level*5),
                            # random.randint(5, 15) + random.randint(0, level*2),
                            1500,
                            Vector2(rand_pos_x, rand_pos_y),
                            5
                        )
                    )
                )
            elif enemyChooser == 3:
                self._enemies.add(
                    ChargeEnemy(
                        EnemyData(
                            random.randint(30, 50) + (level*5),
                            # random.randint(5, 15) + random.randint(0, level*2),
                            1500,
                            Vector2(rand_pos_x, rand_pos_y),
                            5
                        )
                    )
                )
            elif enemyChooser == 5:
                self._enemies.add(
                    EnemyType5(
                        EnemyData(
                            random.randint(30, 50) + (level * 5),
                            # random.randint(5, 15) + random.randint(0, level*2),
                            1500,
                            Vector2(rand_pos_x, rand_pos_y),
                            5,
                            level
                        )
                    )
                )

    def get_enemy_count(self) -> int:
        return len(self._enemies.sprites())

    def update(self, player: PlayerSprite, screen: Surface):
        # enemies need reference to other enemies and the player
        self._enemies.update(player, self._enemies, screen)
        hit = sprite.groupcollide(
            self._enemies, player.bullets, False, True, sprite.collide_mask)
        for enemy in hit:
            enemy.take_damage(player._damage)

    def draw(self, screen: Surface):
        for enemy in self._enemies:
            enemy.draw(screen)
            enemy.bullets.draw(screen)
