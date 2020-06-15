from pygame import Vector2, sprite
from character.enemy.enemy_sprite import EnemySprite
from character.enemy.enemy_data import EnemyData
from character.player.player_sprite import PlayerSprite
from game_settings import WINDOW_HEIGHT


class EnemyManager:
    def __init__(self):
        self._enemies = sprite.Group()

    def spawn_enemies(self):

        self._enemies.add(EnemySprite(EnemyData(50, 4, Vector2(10, 20), 6)))
        self._enemies.add(EnemySprite(
            EnemyData(60, 5, Vector2(300, WINDOW_HEIGHT - 50), 7)))

    def update(self, player: PlayerSprite):
        # enemies need reference to other enemies and the player
        self._enemies.update(player, self._enemies)

    def draw(self, screen):
        self._enemies.draw(screen)
