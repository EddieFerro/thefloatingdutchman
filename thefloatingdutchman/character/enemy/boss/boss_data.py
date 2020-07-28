from enum import Enum

from pygame import Vector2

from thefloatingdutchman.character.enemy.enemy_data import EnemyData


class BossState(Enum):
    ROAM = 0,
    RETURN = 1,
    STATIONARY = 2,
    CHARGE = 3,
    TELEPORT = 4,
    MOVEDOWN = 5,
    MOVEUP = 6
    TRANSITION = 7,
    ENRAGED = 8


class BossData(EnemyData):
    """Enemy class for base enemy can be later subclassed to create specific types of enemies """

    def __init__(self, health: int, attack_speed: int, spawn: Vector2, vel, state, type1, type2, type3):
        super().__init__(health, attack_speed, spawn, vel)
        self._initial_spawn = Vector2(spawn)
        self._state = state
        self._type3 = type3
        self._type2 = type2
        self._type1 = type1

    @property
    def initial_spawn(self) -> Vector2:
        return self._initial_spawn

    @property
    def state(self) -> BossState:
        return self._state

    @state.setter
    def state(self, new_state: BossState) -> None:
        self._state = new_state
