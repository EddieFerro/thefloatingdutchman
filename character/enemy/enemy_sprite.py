from pygame import Surface, Vector2
from pygame.sprite import Group

from character.character_sprite import CharacterSprite
from character.player.player_sprite import PlayerSprite
from character.enemy.enemy_data import EnemyData
from game_settings import GREEN


class EnemySprite(CharacterSprite):
    def __init__(self, enemy_data: EnemyData):
        super().__init__(enemy_data)

    def _set_original_image(self):
        self._original_image = Surface((20, 50))
        self._original_image.fill(GREEN)

    # Enemy AI might go in here
    def update(self, player: PlayerSprite, enemies: Group):
        direction_vector = Vector2(
            - self.rect.x + player.rect.x, - self.rect.y + player.rect.y)
        try:
            direction_vector.scale_to_length(self._data.vel)

            if self.rect.colliderect(player.rect):
                enemies.remove(self)
            self.rect.move_ip(direction_vector)
        except ValueError:
            return
