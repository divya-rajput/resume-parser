from resume_parser.coordinator import ResumeExtractor
from resume_parser.extractors.name_regex import NameRegexExtractor
from resume_parser.extractors.email_regex import EmailRegexExtractor
from resume_parser.extractors.skills_llm import BaseSkillsLLMExtractor


def test_resume_extractor_end_to_end():
    text = """
    Jane Doe
    Senior Engineer
    jane.doe@example.com
    Skills: Python, Machine Learning, LLM
    """

    def fake_llm(prompt: str) -> str:
        return '["Python", "Machine Learning", "LLM"]'
    
    class DummySkillsExtractor(BaseSkillsLLMExtractor):
        def __init__(self, llm_callable):
            self.llm = llm_callable
        
        def extract(self, text: str):
            raw = self.llm(text)
            return self._parse_response(raw)
        
        def extract_skills(self, text: str):
            raw = self.llm(text)
            return self._parse_response(raw)

    extractors = {
        "name": NameRegexExtractor(),
        "email": EmailRegexExtractor(),
        "skills": DummySkillsExtractor(fake_llm),
    }

    extractor = ResumeExtractor(extractors)
    data = extractor.extract(text)

    assert data.name == "Jane Doe"
    assert data.email == "jane.doe@example.com"
    assert data.skills == ["Python", "Machine Learning", "LLM"]