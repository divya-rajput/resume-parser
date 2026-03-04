from abc import ABC, abstractmethod


class FileParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> str:
        """
        Parse the file and return plain text.
        """
        raise NotImplementedError