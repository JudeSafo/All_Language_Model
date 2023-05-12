#!/usr/bin/env python3

import logging
import os
import argparse
from utils import PDFParser, TextPreprocessor

# Configure the logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def pdf_to_text(input_dir:str, output_dir:str=None, filename:str=None) -> None:
    if not os.path.isdir(input_dir):
        logging.error(f"{input_dir} is not a valid directory")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    text_preprocessor = TextPreprocessor()

    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)

        if os.path.isfile(filepath) and filename.endswith(".pdf"):
            output_file = os.path.join(output_dir, f"{filename[:-4]}.txt")

            parser = PDFParser(filepath, output_file, use_ocr=False)
            parser.process_pdf()

            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
            content = text_preprocessor.preprocess(content)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)

            logging.info(f"Output saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from PDF files")
    parser.add_argument(
        "-i",
        "--input_folder",
        type=str,
        help="The input folder containing the PDF files",
    )
    parser.add_argument(
        "-o",
        "--output_folder",
        type=str,
        help="The output folder for the plaintext files",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default="",
        help="The output file name prefix for the plaintext files",
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = args.input_folder or os.path.join(script_dir, "..", "pdfs")

    # Use the provided output folder or default to the "plaintext" folder in the script's parent directory
    plaintext_dir = args.output_folder or os.path.join(script_dir, "..", "plaintext")

    logging.info(f"script_dir: {script_dir}, data_dir: {data_dir}, plaintext_dir: {plaintext_dir}")

    pdf_to_text(data_dir, plaintext_dir, args.filename)
