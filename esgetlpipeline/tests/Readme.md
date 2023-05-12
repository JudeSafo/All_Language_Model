# PDF Parser

This project contains a Python module for parsing text from PDF files using the `pdfplumber` and `pytesseract` libraries.

## Usage

To use this module, you can import the `PDFParser` class from the `my_project` package and create a new instance with the path to your input and output files. Here's an example:

```python
from my_project import PDFParser

input_file = "/path/to/input.pdf"
output_file = "/path/to/output.txt"

parser = PDFParser(input_file, output_file, use_ocr=True)
parser.process_pdf()
```

## Running the Unit Tests

This project includes a set of unit tests to ensure that the PDF parsing functionality is working correctly. To run the unit tests, follow these steps:
Install the project dependencies by running pip install -r requirements.txt in your terminal.
Navigate to the root directory of the project in your terminal.

Run the following command to execute the unit tests:

```bash
Copy code
python -m unittest discover -s tests
```
This will run all of the unit tests in the tests directory and display the results in your terminal.

What is Being Tested
The unit tests in this project are designed to test the functionality of the PDFParser class. There are two test cases:

`test_extract_text_with_pdfplumber`: This test case tests the `extract_text_with_pdfplumber` method of the PDFParser class by creating a new PDFParser instance, calling the method, and then checking that the output file contains the expected text.

`test_extract_text_with_tesseract`: This test case tests the `extract_text_with_tesseract` method of the PDFParser class by creating a new PDFParser instance with OCR enabled, calling the method, and then checking that the output file contains the expected text.
