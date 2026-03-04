from typing import Optional

from .base import FileParser


class WordParser(FileParser):
    """
    Minimal DOCX parser using python-docx unless a backend is injected.
    """

    def __init__(self, backend: Optional[object] = None) -> None:
        self._backend = backend

    def parse(self, file_path: str) -> str:
        backend = self._backend

        if backend is None:
            try:
                import docx  # type: ignore
                backend = docx
            except ImportError as exc:
                raise ImportError(
                    "python-docx is required for DOCX parsing. Install with `pip install python-docx`."
                ) from exc

        document = backend.Document(file_path)
        paragraphs = [p.text for p in document.paragraphs if p.text]

        return "\n".join(paragraphs)