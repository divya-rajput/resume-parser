from abc import ABC, abstractmethod
from typing import Any


class FieldExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> Any:
        """
        Extract a field from the given text.
        Concrete implementations decide the return type.
        """
        raise NotImplementedError