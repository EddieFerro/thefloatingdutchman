from abc import ABC, abstractmethod


class Manager(ABC):
    """Wrapper around sprite group(s) or single sprite"""

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
