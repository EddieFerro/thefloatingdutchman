from typing import List

from pygame import Vector2, Surface, time

from thefloatingdutchman.character.enemy.boss.minion_boss import MinionBoss
from thefloatingdutchman.character.enemy.chase_enemy import ChaseEnemy
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.character.enemy.boss.boss_data import BossData
from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.character.enemy.enemy_manager import EnemyManager
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT


class BossManager(EnemyManager):
    def __init__(self):
        super().__init__()
        self._boss = None

    def _add_enemies(self, level: int):
        self.last_spawn_time = 0

        self._boss = MinionBoss(
            BossData(400, 1500, Vector2(300, WINDOW_HEIGHT/2), 5))
        self._enemies.add(self._boss)

    def update(self, player: PlayerSprite, screen: Surface):
        super().update(player, screen)

        current_time = time.get_ticks()
        if not self.last_spawn_time or current_time - self.last_spawn_time >= 10000:
            curr_dist = self._boss._data.pos.distance_to(
                self._boss._data._initial_spawn)
            if curr_dist < 100:
                self._enemies.add(
                    self._spawn_minions(player)
                )
                self.last_spawn_time = current_time
                self._boss._return_mode = False
            else:
                self._boss._return_mode = True
                self._boss.invulnerable_start = time.get_ticks()

    def _spawn_minions(self, player: PlayerSprite) -> List[EnemySprite]:

        return [
            ChaseEnemy(EnemyData(15, 10, Vector2(600, WINDOW_HEIGHT/2), 10)),
            ChaseEnemy(EnemyData(15, 10, Vector2(
                540, WINDOW_HEIGHT/2 + 100), 10)),
            ChaseEnemy(EnemyData(15, 10, Vector2(
                540, WINDOW_HEIGHT/2 - 100), 10)),
            ChaseEnemy(EnemyData(15, 10, Vector2(
                500, WINDOW_HEIGHT/2 + 200), 10)),
            ChaseEnemy(EnemyData(15, 10, Vector2(
                500, WINDOW_HEIGHT/2 - 200), 10)),
        ]
