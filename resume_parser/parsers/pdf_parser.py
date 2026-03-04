from typing import Optional

from .base import FileParser


class PDFParser(FileParser):
    """
    Minimal PDF parser using PyPDF2 unless a backend is injected.
    """

    def __init__(self, backend: Optional[object] = None) -> None:
        self._backend = backend

    def parse(self, file_path: str) -> str:
        backend = self._backend

        if backend is None:
            try:
                import PyPDF2  # type: ignore
                backend = PyPDF2
            except ImportError as exc:
                raise ImportError(
                    "PyPDF2 is required for PDF parsing. Install with `pip install PyPDF2`."
                ) from exc

        text_chunks = []
        with open(file_path, "rb") as f:
            reader = backend.PdfReader(f)
            for page in reader.pages:
                text_chunks.append(page.extract_text() or "")

        return "\n".join(text_chunks)