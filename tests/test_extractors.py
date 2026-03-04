import textwrap

from resume_parser.extractors.name_regex import NameRegexExtractor
from resume_parser.extractors.email_regex import EmailRegexExtractor
from resume_parser.extractors.skills_llm import BaseSkillsLLMExtractor


def test_name_regex_extractor_detects_name():
    text = textwrap.dedent("""
        Jane Doe
        Senior Software Engineer
        jane.doe@example.com
    """)
    extractor = NameRegexExtractor()
    assert extractor.extract(text) == "Jane Doe"


def test_name_regex_extractor_fallback_to_first_line():
    text = textwrap.dedent("""
        JANE DOE - RESUME
        Skills: Python, ML
    """)
    extractor = NameRegexExtractor()
    assert extractor.extract(text) == "JANE DOE - RESUME"


def test_email_regex_extractor_finds_email():
    text = "Contact me at jane.doe@example.com for details."
    extractor = EmailRegexExtractor()
    assert extractor.extract(text) == "jane.doe@example.com"


def test_email_regex_extractor_returns_empty_when_missing():
    text = "No email here."
    extractor = EmailRegexExtractor()
    assert extractor.extract(text) == ""

def test_parse_response_json_array():
    """BaseSkillsLLMExtractor should correctly parse a JSON array."""

    class DummyExtractor(BaseSkillsLLMExtractor):
        def extract_skills(self, text: str) -> list[str]:
            return self._parse_response(text)

    extractor = DummyExtractor()

    response = '["Python", "SQL", "Docker"]'
    result = extractor._parse_response(response)

    assert result == ["Python", "SQL", "Docker"]


def test_parse_response_json_array_with_spaces():
    """JSON array with extra whitespace should still parse correctly."""

    class DummyExtractor(BaseSkillsLLMExtractor):
        def extract_skills(self, text: str) -> list[str]:
            return self._parse_response(text)

    extractor = DummyExtractor()

    response = '  [ "Python" , " SQL " ]  '
    result = extractor._parse_response(response)

    assert result == ["Python", "SQL"]


def test_parse_response_fallback_csv():
    """If JSON fails, fallback to comma-separated parsing."""

    class DummyExtractor(BaseSkillsLLMExtractor):
        def extract_skills(self, text: str) -> list[str]:
            return self._parse_response(text)

    extractor = DummyExtractor()

    response = "Python, SQL, Docker"
    result = extractor._parse_response(response)

    assert result == ["Python", "SQL", "Docker"]


def test_parse_response_single_value():
    """Single skill should return a single-item list."""

    class DummyExtractor(BaseSkillsLLMExtractor):
        def extract_skills(self, text: str) -> list[str]:
            return self._parse_response(text)

    extractor = DummyExtractor()

    response = "Python"
    result = extractor._parse_response(response)

    assert result == ["Python"]
    
    
def test_dummy_extractor_with_fake_llm():
    """Test a realistic subclass that uses a fake LLM callable."""

    class DummyExtractor(BaseSkillsLLMExtractor):
        def __init__(self, llm_callable):
            self.llm = llm_callable

        def extract_skills(self, text: str) -> list[str]:
            raw = self.llm(text)
            return self._parse_response(raw)

    def fake_llm(_):
        return '["Python", "Machine Learning"]'

    extractor = DummyExtractor(fake_llm)
    result = extractor.extract_skills("resume text")

    assert result == ["Python", "Machine Learning"]


