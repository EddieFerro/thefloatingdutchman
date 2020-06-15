from abc import ABC, abstractmethod


class Manager(ABC):
    """Wrapper around sprite group(s) or single sprite"""

    @abstractmethod
    def spawn(self):
        """should initialize whatever sprites are managed"""

    @abstractmethod
    def update(self):
        """calls update on sprites managed"""

    @abstractmethod
    def draw(self):
        """calls draw on sprites managed"""
