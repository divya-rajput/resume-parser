# Resume Parser

A simple, modular Python framework for extracting information from resumes.

This project demonstrates clean object‑oriented design with pluggable components for parsing and extracting structured data from PDF and DOCX resumes. It includes:
- File parsers for PDF and DOCX
- Extractors for name, email, and skills
- LLM‑powered skill extraction (Ollama, Azure OpenAI, or a simple callable)
- A coordinator that assembles results into a structured model
- A full pytest suite for validation

The framework is lightweight, easy to extend, and designed for clarity and testability.

---

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate

## Install dependencies
pip install -r requirements.txt

## If you don’t have a requirements file
pip install pytest PyPDF2 python-docx

## Running Tests
All tests are located in the tests/ directory.
Run them with:
python -m pytest -q

## Project Structure
resume_parser/
    framework.py
    coordinator.py
    models.py
    parsers/
    extractors/
tests/

## Notes
- PDF parsing uses PyPDF2.
- DOCX parsing uses python-docx.
- Skill extraction can use a simple function or an LLM backend (Ollama, Azure OpenAI).








