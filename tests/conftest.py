"""Shared test fixtures."""
import pytest
from extractors.skills_llm import BaseSkillsLLMExtractor
from parsers.base import FileParser


@pytest.fixture
def dummy_skills_extractor():
    """Reusable DummyExtractor for testing BaseSkillsLLMExtractor."""
    class DummyExtractor(BaseSkillsLLMExtractor):
        def extract_skills(self, text: str) -> list[str]:
            return self._parse_response(text)
    return DummyExtractor()


@pytest.fixture
def dummy_skills_extractor_with_llm():
    """Reusable DummyExtractor with fake LLM callable."""
    class DummyExtractor(BaseSkillsLLMExtractor):
        def __init__(self, llm_callable):
            self.llm = llm_callable
        
        def extract(self, text: str):
            raw = self.llm(text)
            return self._parse_response(raw)
        
        def extract_skills(self, text: str):
            raw = self.llm(text)
            return self._parse_response(raw)
    
    def fake_llm(prompt: str) -> str:
        return '["Python", "Machine Learning", "LLM"]'
    
    return DummyExtractor(fake_llm)


@pytest.fixture
def dummy_pdf_parser():
    """Reusable DummyPDFParser for testing FileParser."""
    dummy_text = "Jane Doe\njane.doe@example.com\nSkills: Python"
    
    class DummyPDFParser(FileParser):
        def parse(self, file_path: str) -> str:
            return dummy_text
    
    return DummyPDFParser()
