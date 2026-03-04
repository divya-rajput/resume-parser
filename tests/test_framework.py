from framework import ResumeParserFramework
from coordinator import ResumeExtractor
from extractors.name_regex import NameRegexExtractor
from extractors.email_regex import EmailRegexExtractor
from extractors.skills_llm import BaseSkillsLLMExtractor
from parsers.base import FileParser
import parsers as parser_module # Import the actual parser module

def test_framework_selects_correct_parser(monkeypatch, tmp_path):
    # 1. Setup fake file
    pdf_file = tmp_path / "resume.pdf"
    pdf_file.write_bytes(b"fake")

    # Use cleandoc or left-aligned strings to avoid regex issues with leading whitespace
    dummy_text = "Jane Doe\njane.doe@example.com\nSkills: Python"

    # 2. Define the Mock Parser
    class DummyPDFParser(FileParser):
        def parse(self, file_path: str) -> str:
            return dummy_text

    # 3. PATCH THE CORRECT LOCATION
    # The framework does: getattr(parser_module, "PDFParser")
    # So we must put DummyPDFParser into parser_module.
    monkeypatch.setattr(parser_module, "PDFParser", DummyPDFParser, raising=False)

    # 4. Setup Extractors
    def fake_llm(prompt: str) -> str:
        return '["Python"]'
    
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

    # 5. Execute
    coordinator = ResumeExtractor(extractors)
    framework = ResumeParserFramework(coordinator)
    data = framework.parse_resume(str(pdf_file))

    # 6. Assertions (Using dict access, change to data.name if using DotDict/Dataclasses)
    assert data.name.strip() == "Jane Doe"
    assert data.email.strip() == "jane.doe@example.com"
    assert data.skills == ["Python"]