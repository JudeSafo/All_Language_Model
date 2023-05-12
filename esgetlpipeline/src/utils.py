#!/usr/bin/env python3

# Version: 1.0
# Changes: Initial version of the script.
# Usage: python3 PDFParser <number>
# Example: python3 src/main.py

import os
import re
import datetime
import textwrap
from typing import List
import PyPDF2
import pdfplumber
import pytesseract
import numpy as np
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


def get_timestamp():
    """
    Returns a timestamp in the format YYYY-MM-DD HH:MM:SS.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class PDFParser:
    """
    A class for parsing text from PDF files.
    """

    def __init__(self, input_file: str, output_file: str, use_ocr=False):
        """
        Constructs a new instance of the PDFParser class.

        Args:
            input_file (str): The path to the input PDF file.
            output_file (str): The path to the output text file.
            use_ocr (bool): Whether to use OCR to extract text from the PDF. Defaults to False.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.use_ocr = use_ocr

    def process_pdf(self) -> None:
        """
        Processes the PDF file and extracts text to the output file.
        """
        if not self.use_ocr:
            self.extract_text_with_pdfplumber()
        else:
            self.extract_text_with_tesseract()

    def extract_text_with_pdfplumber(self) -> None:
        """
        Extracts text from the PDF file using pdfplumber and writes it to the output file.
        """
        def write_text(text: str, outfile) -> None:
            outfile.write(text + "\n\n")

        try:
            with pdfplumber.open(self.input_file) as pdf:
                with open(self.output_file, "w", encoding="utf-8") as outfile:
                    for page in pdf.pages:
                        if hasattr(page, "columns"):
                            for column in page.columns:
                                text = column.extract_text()
                                write_text(text, outfile)
                        else:
                            text = page.extract_text()
                            write_text(text, outfile)
        except pdfplumber.pdfparser.PDFSyntaxError as e:
            print(f"[{get_timestamp()}] Error parsing PDF file {self.input_file}: {e}")


    def extract_text_with_tesseract(self) -> None:
        """
        Extracts text from the PDF file using OCR with pytesseract and writes it to the output file.
        """
        pytesseract.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"  # Update this path to match your tesseract executable path
        with pdfplumber.open(self.input_file) as pdf:
            with open(self.output_file, "w", encoding="utf-8") as outfile:
                for page in pdf.pages:
                    img = page.to_image(resolution=300)
                    text = pytesseract.image_to_string(img, lang="eng")
                    outfile.write(text + "\n\n")


class TextPreprocessor:
    def __init__(self):
        self.stop_words = set()
        self._load_stopwords()

    def preprocess(self, content: str) -> str:
        # Remove carriage returns
        content = content.replace("\r", "")

        # Replace line breaks with a space if the preceding character is not a sentence-ending punctuation mark
        content = re.sub(r"(?<![.?!])\n", " ", content)

        # Split the text by delimiter (all caps lines)
        delimiter = r"\n\b(?:[A-Z]+\s*){2,}\b(?!\w)"
        paragraphs = re.split(delimiter, content)

        # Rejoin the paragraphs with two line breaks
        content = "\n\n".join(paragraphs)

        # Reformat the paragraphs using textwrap.fill
        formatted_paragraphs = [
            textwrap.fill(paragraph, width=80) for paragraph in paragraphs
        ]

        # Rejoin the formatted paragraphs with two line breaks
        content = "\n\n".join(formatted_paragraphs)

        return content

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocesses the text by removing stop words and lowercasing the text.

        Returns:
            str: The preprocessed text.
        """
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        tokens = tokenizer.tokenize(self.text.lower())
        tokens = [token for token in tokens if token not in self.stop_words]
        return " ".join(tokens)

    def _load_stopwords(self) -> None:
        cache_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "stopwords.txt"
        )
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                self.stop_words = set(f.read().split())
        else:
            nltk.download("stopwords")
            self.stop_words = set(stopwords.words("english"))
            with open(cache_path, "w") as f:
                f.write(" ".join(self.stop_words))


class TextAggregator(TextPreprocessor):
    """
    Aggregates all text files in a given directory into a single string.

    Args:
        - input_path (str): The directory path.

    Returns:
        - text (str): The aggregated text from all the text files.

    """

    def __init__(self, input_path=None):
        super().__init__()
        if input_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            plaintext_dir = os.path.join(script_dir, "..", "plaintext")
            self.input_path = plaintext_dir
        else:
            self.input_path = input_path
        self.text = ""

    def aggregate(self) -> None:
        if os.path.isfile(self.input_path):
            with open(self.input_path, "r", encoding="utf-8") as f:
                content = f.read()
            content = self.preprocess(content)
            # content = self._preprocess_text(content)
            self.text += content
            print(f"[{get_timestamp()}] Processed file: {self.input_path}")
        elif os.path.isdir(self.input_path):
            for root, dirs, files in os.walk(self.input_path):
                for file in files:
                    if file.endswith(".txt"):
                        print(f"[{get_timestamp()}] Processed file: {file}")
                        file_path = os.path.join(root, file)
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        content = self.preprocess(content)
                        self.text += content
        else:
            raise ValueError("Invalid input path")

        return self.text


class TokenTfidfExtractor(TextPreprocessor):
    def __init__(self, input_path: str, n: int, tokens: List[str]):
        """
        Initializes the TokenTfidfExtractor class.

        Args:
            input_path (str): The path to the input file or directory.
            n (int): The number of top features to extract.
            tokens (List[str]): A list of tokens to find the most closely associated terms.
        """
        super().__init__()
        self.input_path = input_path
        self.n = n if n is not None else 15
        self.tokens = [token.lower() for token in tokens]
        self.text = ""

        # Load stopwords
        self._load_stopwords()

    def _extract_tfidf_features(self) -> None:
        """
        Extracts the top n tf-idf features from the text.

        Returns:
            None.
        """
        if self.text is None:
            print(f"{get_timestamp()} Error: Text is None")
            return

        vectorizer = TfidfVectorizer(ngram_range=(1, 3), norm="l2", use_idf=True)
        X = vectorizer.fit_transform([self.text])
        self.features = vectorizer.vocabulary_.keys()
        self.tfidf = X.toarray().flatten()

        # Sort the n-gram frequency distributions in descending order
        sorted_indices = np.argsort(self.tfidf)[::-1]
        self.features = list(self.features)
        self.tfidf = list(self.tfidf)

        # Print the top n most common n-grams associated with the provided tokens
        for token in self.tokens:
            print(f"{get_timestamp()} Top {self.n} features associated with '{token}':")
            top_tfidf_features = []
            for i, feature in enumerate(self.features):
                tfidf_score = self.tfidf[i]
                num_subtokens = sum(
                    [subtoken in feature.split() for subtoken in token.split()]
                )
                if num_subtokens > 0:
                    top_tfidf_features.append((feature, tfidf_score, num_subtokens))
            top_tfidf_features = list(
                filter(lambda x: x is not None, top_tfidf_features)
            )
            top_tfidf_features.sort(key=lambda x: (x[2], x[1]), reverse=True)
            for i in range(min(self.n, len(top_tfidf_features))):
                feature, tfidf_score = top_tfidf_features[i][:2]
                print(f"{feature}: {tfidf_score*100:.2f}%")
            print()

    def extract_features(self) -> None:
        """
        Extracts the top n tf-idf features from the text.

        Returns:
            None.
        """
        # Load the text from the input file or directory
        if self.input_path.endswith(".txt"):
            with open(self.input_path, "r", encoding="utf-8") as f:
                self.text += f.read()
        elif os.path.isdir(self.input_path):
            text_aggregator = TextAggregator(self.input_path)
            self.text = text_aggregator.aggregate()
        elif isinstance(self.input_path, str):
            self.text = self.input_path
        else:
            raise ValueError("Invalid input path")

        # Preprocess the text
        self.text = self._preprocess_text(self.text)

        # Extract the top n tf-idf features
        self._extract_tfidf_features()
