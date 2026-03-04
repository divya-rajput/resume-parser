from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ResumeData:
    name: str
    email: str
    skills: List[str]