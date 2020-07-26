from abc import ABC, abstractmethod

from thefloatingdutchman.utility.resource_container import ResourceContainer


class Manager(ABC):
    """Wrapper around sprite group(s) or single sprite"""

    def __init__(self, res_container: ResourceContainer):
        super().__init__()
        self._res_container = res_container

    @abstractmethod
    def spawn(self):
        """Should reset state of whatever is being managed"""

    @abstractmethod
    def update(self):
        """
        Updates objects being managed each clock cycle.
        For sprites this is done by calling their update method
        """

    @abstractmethod
    def draw(self):
        """Draws sprites managed to screen"""
