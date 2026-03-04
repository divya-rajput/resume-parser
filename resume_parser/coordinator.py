from typing import Mapping, Dict, List

from .models import ResumeData
from .extractors.base import FieldExtractor


class ResumeExtractor:
    """
    Coordinates field extraction using a mapping:
        {
            "name": NameExtractor,
            "email": EmailExtractor,
            "skills": SkillsExtractor
        }

    Produces a ResumeData object.
    """

    def __init__(self, extractors: Mapping[str, FieldExtractor]) -> None:
        # Make a defensive copy
        self._extractors: Dict[str, FieldExtractor] = dict(extractors)

    def extract(self, text: str) -> ResumeData:
        # Validate required fields
        required = ("name", "email", "skills")
        missing = [field for field in required if field not in self._extractors]

        if missing:
            raise ValueError(f"Missing extractors for fields: {', '.join(missing)}")

        name_extractor = self._extractors["name"]
        email_extractor = self._extractors["email"]
        skills_extractor = self._extractors["skills"]

        name = str(name_extractor.extract(text))
        email = str(email_extractor.extract(text))
        skills_raw = skills_extractor.extract(text)

        # Normalize skills into a list of strings
        if isinstance(skills_raw, (list, tuple)):
            skills: List[str] = [str(s).strip() for s in skills_raw if str(s).strip()]
        else:
            skills = [str(skills_raw)] if skills_raw else []

        return ResumeData(name=name, email=email, skills=skills)