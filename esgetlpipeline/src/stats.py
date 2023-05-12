#!/usr/bin/env python3

import os
import argparse
from typing import List
from utils import TextAggregator
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk
from nltk.corpus import stopwords


class TextTfidfExtractor:
    """
    Extracts the top n tf-idf features from a text file or a collection of text files in a given directory.

    Args:
        - input_path (str): The path to the input file or the directory containing the text files.
        - n (int): The number of top features to extract.

    Returns:
        - None.

    """

    def __init__(self, input_path: str, n: int):
        self.input_path = input_path
        self.n = n
        self.stop_words = set()
        self.text = ""
        self.tfidf = None
        self.features = None

        self._load_stopwords()

    def _load_stopwords(self) -> None:
        """
        Loads stopwords from cache or downloads and caches them.

        Returns:
        - None.

        """
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

    def _preprocess_text(self) -> None:
        """
        Preprocesses the text by removing stop words and lowercasing the text.

        Returns:
        - None.

        """
        self.text = " ".join(
            [word for word in self.text.lower().split() if word not in self.stop_words]
        )

    def _extract_tfidf_features(self) -> None:
        """
        Extracts the top n tf-idf features from the text.

        Returns:
        - None.

        """
        vectorizer = TfidfVectorizer(ngram_range=(1, 3), norm="l2", use_idf=True)
        X = vectorizer.fit_transform([self.text])
        self.features = vectorizer.vocabulary_.keys()
        self.tfidf = X.toarray().flatten()

        # Sort the n-gram frequency distributions in descending order
        sorted_indices = np.argsort(self.tfidf)[::-1]
        self.features = list(self.features)
        self.tfidf = list(self.tfidf)

        # Print the top n most common n-grams
        for i in range(self.n):
            index = sorted_indices[i]
            print(f"{self.features[index]}: {self.tfidf[index]*100:.2f}%")

    def extract_features(self) -> None:
        """
        Extracts the top n tf-idf features from the text.

        Returns:
        - None.

        """
        # Load the text from the input file or directory
        if self.input_path.endswith(".txt"):
            with open(self.input_path, "r", encoding="utf-8") as f:
                self.text += f.read()
        elif os.path.isdir(self.input_path):
            text_aggregator = TextAggregator(self.input_path)
            self.text = text_aggregator.aggregate()
        else:
            raise ValueError("Invalid input path")

        # Preprocess the text
        self._preprocess_text()

        # Extract the top n tf-idf features
        self._extract_tfidf_features()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract the top n tf-idf features from a text file or a collection of text files in a given directory"
    )
    parser


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract the top n tf-idf features from a text file or a collection of text files in a given directory"
    )
    parser.add_argument(
        "-i",
        "--input_path",
        type=str,
        help="the path to the input file or the directory containing the text files",
    )
    parser.add_argument(
        "-n", "--n", type=int, default=15, help="the number of top features to extract"
    )

    args = parser.parse_args()

    if args.input_path:
        # Extract features from input file or directory specified by user
        text_tfidf_extractor = TextTfidfExtractor(args.input_path, args.n)
        text_tfidf_extractor.extract_features()
    else:
        # Extract features from default directory (../plaintext)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        plaintext_dir = os.path.join(script_dir, "..", "plaintext")

        text_tfidf_extractor = TextTfidfExtractor(plaintext_dir, args.n)
        text_tfidf_extractor.extract_features()


"""
import os
import numpy as np
import nltk
from nltk.corpus import stopwords
from utils import TextAggregator
from sklearn.feature_extraction.text import TfidfVectorizer

# Load stopwords from cache or download and cache them
cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stopwords.txt")
if os.path.exists(cache_path):
    with open(cache_path, "r") as f:
        stop_words = set(f.read().split())
else:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))
    with open(cache_path, "w") as f:
        f.write(" ".join(stop_words))


# Check for command line argument specifying directory or file path
if len(sys.argv) > 1:
    input_path = sys.argv[1]
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "plaintext")

# Aggregate text files into a single string
text_aggregator = TextAggregator(input_path)
text = text_aggregator.aggregate()

# Remove stop words
text = " ".join([word for word in text.lower().split() if word not in stop_words])

vectorizer = TfidfVectorizer(ngram_range=(1, 3), norm="l2", use_idf=True)
X = vectorizer.fit_transform([text])
features = vectorizer.vocabulary_.keys()
tfidf = X.toarray().flatten()

# Sort the n-gram frequency distributions in descending order
sorted_indices = np.argsort(tfidf)[::-1]

# Get the list of feature names
feature_names = list(features)

# Print the top 10 most common n-grams
for i in range(15):
    index = sorted_indices[i]
    print(f"{feature_names[index]}: {tfidf[index]*100:.2f}%")
"""
