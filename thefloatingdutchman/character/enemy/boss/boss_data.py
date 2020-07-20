from pygame import Vector2

from thefloatingdutchman.character.enemy.enemy_data import EnemyData


class BossData(EnemyData):
    """Enemy class for base enemy can be later subclassed to create specific types of enemies """
    # Will make sure to subclass enemy types later on

    def __init__(self, health: int, attack_speed: int, spawn: Vector2, vel):
        super().__init__(health, attack_speed, spawn, vel)
        self._initial_spawn = spawn
        self._stopMoving = False
