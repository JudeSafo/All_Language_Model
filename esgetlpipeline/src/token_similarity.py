#!/usr/bin/env python3

import os
import argparse
from nltk.corpus import stopwords
from utils import TokenTfidfExtractor


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
    parser.add_argument(
        "-t",
        "--tokens",
        type=str,
        default="",
        help="comma-separated list of tokens to find the most closely associated terms",
    )

    args = parser.parse_args()

    tokens = [token.strip().lower() for token in args.tokens.split(",")]
    if args.input_path:
        # Extract features from input file or directory specified by user
        text_tfidf_extractor = TokenTfidfExtractor(args.input_path, args.n, tokens)

        # Print the first 100 characters of the text
        # print(f"First 100 characters of the text: {text_tfidf_extractor.text[:100]}")

        text_tfidf_extractor.extract_features()
    else:
        # Extract features from default directory (../plaintext)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        plaintext_dir = os.path.join(script_dir, "..", "plaintext")

        text_tfidf_extractor = TokenTfidfExtractor(plaintext_dir, args.n, tokens)

        # Print the first 100 characters of the text
        # print(f"First 100 characters of the text: {text_tfidf_extractor.text[:100]}")

        text_tfidf_extractor.extract_features()
