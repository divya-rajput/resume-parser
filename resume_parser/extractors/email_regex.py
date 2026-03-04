import re

from .base import FieldExtractor


class EmailRegexExtractor(FieldExtractor):
    """
    Regex-based email extractor.

    Returns the first email found, or an empty string if none.
    """

    EMAIL_PATTERN = re.compile(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    def extract(self, text: str) -> str:
        match = self.EMAIL_PATTERN.search(text)
        return match.group(0) if match else ""