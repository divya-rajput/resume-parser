# Resume Parser

A modular Python framework for extracting structured information from resumes (PDF and DOCX files).

## Overview

This project demonstrates clean object-oriented design with pluggable components. It provides:

- **File Parsers**: Extract plain text from PDF and DOCX resume files
- **Field Extractors**: 
  - `NameRegexExtractor`: Extract name using regex patterns
  - `EmailRegexExtractor`: Extract email using regex patterns
  - `BaseSkillsLLMExtractor`: Extract skills using LLM backends (Ollama, Azure OpenAI, or custom callables)
- **ResumeExtractor (Coordinator)**: Orchestrates extractors to produce structured `ResumeData`
- **ResumeParserFramework**: High-level orchestrator that handles file parsing and extraction end-to-end
- **Data Model**: `ResumeData` dataclass with `name`, `email`, and `skills` fields

## Installation

[Optional] Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirement.txt
```

Dependencies:
- `pytest` - Testing framework
- `PyPDF2` - PDF parsing
- `python-docx` - DOCX parsing
- `ollama` - Optional: Ollama LLM backend
- `openai` - Optional: Azure OpenAI backend

## Running Tests

All tests are located in the `tests/` directory.

```bash
python -m pytest -q
```

## Project Structure

```
.
├── framework.py           # High-level orchestrator for file parsing and extraction
├── coordinator.py         # ResumeExtractor - coordinates field extraction
├── models.py              # ResumeData dataclass
├── extractors/            # Field extractors
│   ├── base.py            # FieldExtractor abstract base class
│   ├── name_regex.py      # Name extraction via regex
│   ├── email_regex.py     # Email extraction via regex
│   └── skills_llm.py      # Skills extraction via LLM
├── parsers/               # File parsers
│   ├── base.py            # FileParser abstract base class
│   ├── pdf_parser.py      # PDF parsing using PyPDF2
│   └── word_parser.py     # DOCX parsing using python-docx
└── tests/                 # Test suite (13 tests)
```

## Usage Example

```python
from coordinator import ResumeExtractor
from extractors.name_regex import NameRegexExtractor
from extractors.email_regex import EmailRegexExtractor
from extractors.skills_llm import BaseSkillsLLMExtractor
from framework import ResumeParserFramework

# 1. Define a custom LLM-powered skills extractor
class MySkillsExtractor(BaseSkillsLLMExtractor):
    def extract(self, text: str):
        # Call your LLM and parse response
        raw = self.llm(text)
        return self._parse_response(raw)
    
    def extract_skills(self, text: str):
        raw = self.llm(text)
        return self._parse_response(raw)

# 2. Create extractors
extractors = {
    "name": NameRegexExtractor(),
    "email": EmailRegexExtractor(),
    "skills": MySkillsExtractor(llm_callable),
}

# 3. Coordinate extraction
coordinator = ResumeExtractor(extractors)
resume_data = coordinator.extract(text)

# Or use the framework for end-to-end processing
framework = ResumeParserFramework(coordinator)
resume_data = framework.parse_resume("path/to/resume.pdf")

print(resume_data.name)    # e.g., "Jane Doe"
print(resume_data.email)   # e.g., "jane.doe@example.com"
print(resume_data.skills)  # e.g., ["Python", "Machine Learning"]
```

## Design Principles

- **Modularity**: Each component (parser, extractor, coordinator) is independent and testable
- **Extensibility**: Implement `FileParser` or `FieldExtractor` to add custom parsers/extractors
- **Testability**: Abstract base classes and dependency injection enable mocking and testing
- **Flexibility**: Works with any LLM backend via callable pattern
