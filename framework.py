from pathlib import Path
from typing import Dict, Type

from models import ResumeData
from parsers.base import FileParser
from parsers.pdf_parser import PDFParser
from parsers.word_parser import WordParser


class ResumeParserFramework:
    """
    High-level orchestrator that:
    - Selects the correct FileParser based on file extension.
    - Uses ResumeExtractor to extract structured fields.
    """

    # Store class names instead of class objects
    _PARSERS: Dict[str, str] = {
        ".pdf": "PDFParser",
        ".docx": "WordParser",
    }

    def __init__(self, resume_extractor):
        self._resume_extractor = resume_extractor

    def _select_parser(self, file_path: str) -> FileParser:
        suffix = Path(file_path).suffix.lower()
        parser_name = self._PARSERS.get(suffix)

        if parser_name is None:
            raise ValueError(f"Unsupported file type: {suffix}")

        # Import dynamically so monkeypatching works
        import parsers as parser_module

        parser_cls: Type[FileParser] = getattr(parser_module, parser_name)
        return parser_cls()

    def parse_resume(self, file_path: str) -> ResumeData:
        parser = self._select_parser(file_path)
        text = parser.parse(file_path)
        return self._resume_extractor.extract(text)