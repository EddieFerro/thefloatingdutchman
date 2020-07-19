import random
from typing import List

from pygame import Vector2, sprite, Surface, time

from thefloatingdutchman.character.enemy.boss.minion_boss import MinionBoss
from thefloatingdutchman.character.enemy.chase_enemy import ChaseEnemy
from thefloatingdutchman.character.enemy.ranged_enemy import RangedEnemy
from thefloatingdutchman.character.enemy.ranged_teleport_enemy import RangedTeleportEnemy
from thefloatingdutchman.character.enemy.charge_enemy import ChargeEnemy
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.character.enemy.enemy_manager import EnemyManager
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from thefloatingdutchman.manager import Manager


class BossManager(EnemyManager):
    def __init__(self):
        super().__init__()
        self.last_spawn_time = 0
        self._boss = None

    def _add_enemies(self, level: int):

        self._boss = MinionBoss(
            EnemyData(400, 1500, Vector2(100, 100), 5))
        self._enemies.add(self._boss)

    def update(self, player: PlayerSprite, screen: Surface):
        super().update(player, screen)

        current_time = time.get_ticks()
        if not self.last_spawn_time or current_time - self.last_spawn_time >= 20000:
            self._enemies.add(
                self._spawn_minions(player)
            )
            self.last_spawn_time = current_time

    def _spawn_minions(self, player: PlayerSprite) -> List[EnemySprite]:

        enemy_pos = (self._boss._data.pos + player._data.pos)/2

        return [
            ChaseEnemy(EnemyData(15, 10, Vector2(
                enemy_pos.x + (i*20), enemy_pos.y + (i*20)), 10))
            for i in range(0, random.randint(3, 6))
        ]
