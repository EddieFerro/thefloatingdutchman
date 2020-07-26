from abc import ABC, abstractmethod

from pygame.sprite import Group
from pygame import Surface

from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.utility.resource_container import ResourceContainer
from thefloatingdutchman.objects.weapons.enemy_weapon import EnemyWeapon


class WeaponEnemy(EnemySprite, ABC):
    def __init__(self, res_container: ResourceContainer, enemy_data: EnemyData):
        super().__init__(res_container, enemy_data)
        self._weapon = EnemyWeapon(res_container)
        self._weapon.spawn()

    @abstractmethod
    def _set_original_image(self, res_container: ResourceContainer):
        pass

    @abstractmethod
    def update(self, player: PlayerSprite, enemies: Group, screen: Surface):
        pass

    @property
    def weapon(self) -> EnemyWeapon:
        return self._weapon
