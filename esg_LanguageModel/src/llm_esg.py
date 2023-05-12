#!/usr/bin/env python3
"""
Name: llm_esg.py
Description: A script to process user input text, find matching keys in a JSON file, and generate a summary based on the matched keys' values using Hugging Face's summarization model.

Usage:
    python text_processor.py -i "Input text goes here" -p path/to/your/json_file.json -o path/to/output/folder

Arguments:
    input_text: The input text provided by the user (less than 64 tokens)
    json_file: Path to the JSON file containing the schema
    -o, --output: Optional argument specifying the output folder (defaults to the current location if not provided)

Example:
    python text_processor.py "Stark Industries is committed to sustainability and delivering a positive impact on the world." example.json -o output
"""

import re
import json
import sys
import os
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Tuple
from transformers import pipeline

logging.basicConfig(level=logging.ERROR)  # Set log level to ERROR to suppress warnings

def log(message: str) -> None:
    """Log messages with timestamps to stdout."""
    print(f"[{datetime.now()}] {message}")

class TextProcessor:
    def __init__(self, input_text: str, json_file: str):
        self.input_text = input_text
        self.json_data = self.load_json(json_file)
        self.summary_model = pipeline("summarization")

    def load_json(self, json_file: str) -> Dict:
        """Load JSON data from a file."""
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
            return data
        except Exception as e:
            log(f"Error loading JSON data: {e}")
            sys.exit(1)

    def find_relevant_keys(self) -> List[str]:
        """Find JSON keys that match the token expressions from the input text."""
        relevant_keys = []
        for key, value in self.json_data.items():
            for expression in value.keys():
                if re.search(r'\b' + expression + r'\b', self.input_text, re.IGNORECASE):
                    relevant_keys.append(expression)
                    break
        return relevant_keys


    def generate_paragraph(self, relevant_keys: List[str]) -> str:
        """Create a paragraph based on the values corresponding to the matched keys."""
        paragraph = ""
        max_size = 4096  # Set the maximum size limit for the aggregated paragraph
        visited_keys = set()  # Keep track of keys that have already been used
        for key in relevant_keys:
            if len(paragraph) >= max_size:  # Stop adding more text if the limit is reached
                break
            for main_key, main_key_data in self.json_data.items():
                if key in main_key_data and key not in visited_keys:
                    key_data = main_key_data[key]
                    for entry in key_data:
                        if len(paragraph) + len(entry["text"]) < max_size:
                            paragraph += entry["text"] + " "
                        else:
                            break
                    visited_keys.add(key)
        return paragraph

    def generate_summary(self, paragraph: str) -> str:
        """Generate a summary using Hugging Face's summarization model."""
        try:
            summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")
            summary = self.summary_model(paragraph, min_length = 5, max_length=len(paragraph) + len(self.summary_model.tokenizer(self.input_text)['input_ids']), do_sample=False)
            #summary = self.summary_model(paragraph, max_length=150)
            return summary[0]["summary_text"]
        except Exception as e:
            log(f"Error generating summary: {e}")
            sys.exit(1)

    def run(self) -> Dict:
        """Run the text processing and summarization."""
        relevant_keys = self.find_relevant_keys()
        paragraph = self.generate_paragraph(relevant_keys)
        summary = self.generate_summary(paragraph)

        result = {
            "input_text": self.input_text,
            "summary": [{"summary_text": summary}],
            "relevant_search_terms": relevant_keys,
            "aggregated_paragraph": paragraph,
        }

        return result


def main():
    parser = argparse.ArgumentParser(description="Generate a summary based on input text and a JSON file.")
    parser.add_argument("-i", "--input_text", help="Input text provided by the user", default=None)
    parser.add_argument("-p", "--json_path", help="Path to the JSON file", required=True)
    parser.add_argument("-o", "--output", help="Path to the output folder", default=".")

    args = parser.parse_args()

    if args.input_text is None:
        args.input_text = input("Please enter input text: ")

    processor = TextProcessor(args.input_text, args.json_path)
    result = processor.run()

    output_file = os.path.join(args.output, "output.json")

    try:
	    with open(output_file, "w") as f:
		    json.dump(result, f, indent=2)
    except Exception as e:
        log(f"Error writing output to file: {e}")
        sys.exit(1)

    log(f"Output written to {output_file}")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

