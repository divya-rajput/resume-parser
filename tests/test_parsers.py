from resume_parser.parsers.pdf_parser import PDFParser
from resume_parser.parsers.word_parser import WordParser


# ---------- PDF Dummies ----------

class DummyPDFPage:
    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class DummyPDFReader:
    def __init__(self, file_obj):
        self.pages = [
            DummyPDFPage("Hello"),
            DummyPDFPage("World")
        ]


class DummyPDFBackend:
    PdfReader = DummyPDFReader


def test_pdf_parser_with_dummy_backend(tmp_path):
    pdf_file = tmp_path / "resume.pdf"
    pdf_file.write_bytes(b"fake pdf bytes")

    parser = PDFParser(backend=DummyPDFBackend)
    text = parser.parse(str(pdf_file))

    assert "Hello" in text
    assert "World" in text


# ---------- DOCX Dummies ----------

class DummyParagraph:
    def __init__(self, text):
        self.text = text


class DummyDoc:
    def __init__(self, path):
        self.paragraphs = [
            DummyParagraph("Line 1"),
            DummyParagraph("Line 2")
        ]


class DummyDocxBackend:
    def Document(self, path):
        return DummyDoc(path)


def test_word_parser_with_dummy_backend(tmp_path):
    docx_file = tmp_path / "resume.docx"
    docx_file.write_bytes(b"fake docx bytes")

    parser = WordParser(backend=DummyDocxBackend())
    text = parser.parse(str(docx_file))

    assert "Line 1" in text
    assert "Line 2" in text