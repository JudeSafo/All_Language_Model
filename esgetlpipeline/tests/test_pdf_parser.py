import os
import unittest
from my_project import PDFParser

class TestPDFParser(unittest.TestCase):
    def setUp(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_file = os.path.join(self.script_dir, 'data', 'test.pdf')
        self.output_file = os.path.join(self.script_dir, 'test_output.txt')

    def tearDown(self):
        os.remove(self.output_file)

    def test_extract_text_with_pdfplumber(self):
        parser = PDFParser(self.input_file, self.output_file, use_ocr=False)
        parser.extract_text_with_pdfplumber()
        with open(self.output_file, 'r', encoding='utf-8') as f:
            text = f.read()
            self.assertIn("This is a test PDF file.", text)

    def test_extract_text_with_tesseract(self):
        parser = PDFParser(self.input_file, self.output_file, use_ocr=True)
        parser.extract_text_with_tesseract()
        with open(self.output_file, 'r', encoding='utf-8') as f:
            text = f.read()
            self.assertIn("This is a test PDF file.", text)

if __name__ == '__main__':
    unittest.main()

