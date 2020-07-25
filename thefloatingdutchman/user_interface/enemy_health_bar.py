from pygame import draw, Surface, Rect, Vector2

from thefloatingdutchman.game_settings import RED, BLACK


class EnemyHealthBar():
    def __init__(self, health: int, enemy_rect: Rect):
        self._enemy_width = enemy_rect.width
        self._enemy_height = enemy_rect.height
        self._init_health = health

    def draw(self, screen: Surface, enemy_pos: Vector2, current_health: int):

        start_cord = (enemy_pos.x - (self._enemy_width/2),
                      enemy_pos.y - (self._enemy_height/2) - 20)

        black_rect = Rect(start_cord, (self._enemy_width, 10))
        health_rect = Rect(start_cord, (self._enemy_width *
                                        (current_health/self._init_health), 10))
        draw.rect(screen, BLACK, black_rect)
        draw.rect(screen, RED, health_rect)
