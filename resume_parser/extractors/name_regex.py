import re
from typing import Optional, List

from .base import FieldExtractor


class NameRegexExtractor(FieldExtractor):
    """
    Simple heuristic name extractor.

    Strategy:
    - Scan the first few non-empty lines for a “Name-like” pattern.
    - Fallback to the first non-empty line if no pattern matches.
    """

    NAME_PATTERN = re.compile(r"^[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)+$")

    def __init__(self, max_lines_to_scan: int = 5) -> None:
        self.max_lines_to_scan = max_lines_to_scan

    def extract(self, text: str) -> str:
        lines: List[str] = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return ""

        match = self._find_pattern_match(lines)
        return match if match is not None else lines[0]

    def _find_pattern_match(self, lines: list[str]) -> Optional[str]:
        for line in lines[: self.max_lines_to_scan]:
            if self.NAME_PATTERN.match(line):
                return line
        return None