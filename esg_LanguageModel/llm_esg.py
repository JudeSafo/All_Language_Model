#!/usr/bin/env python3
"""
Name: llm_esg.py
Description: A script to process user input text, find matching keys in a JSON file, and generate a summary based on the matched keys' values using Hugging Face's summarization model.

Usage:
    python llm_esg.py -i "Input text goes here" -p path/to/your/json_file.json -o path/to/output/folder

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
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import AutoModelForQuestionAnswering, pipeline

logging.basicConfig(level=logging.ERROR)  # Set log level to ERROR to suppress warnings

def log(message: str) -> None:
    """Log messages with timestamps to stdout."""
    print(f"[{datetime.now()}] {message}")

class QuestionAnswerModel:
    def __init__(self, question: str, reference_text: str, model, tokenizer):
        """
        Initializes the QuestionAnswerModel with the given question and reference text.

        :param question: The question to be answered.
        :type question: str
        :param reference_text: The reference text to find the answer in.
        :type reference_text: str
        """
        self.question = question
        self.reference_text = reference_text
        self.model = model
        self.tokenizer = tokenizer

    def get_answer(self) -> str:
        """
        Returns the answer to the given question based on the provided reference text.

        :return: The answer to the question.
        :rtype: str
        """
        try:
            model_name = "deepset/roberta-base-squad2"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForQuestionAnswering.from_pretrained(model_name)
            max_answer_len = 200

            qa_pipeline = pipeline("question-answering", model=self.model, tokenizer=self.tokenizer, max_answer_len=max_answer_len)
            result = qa_pipeline({"question": self.question, "context": self.reference_text})
            return result["answer"]
        except Exception as e:
            print(f"Error while getting answer: {str(e)}")
            return "An error occurred while trying to find an answer."


class TextProcessor:
    def __init__(self, input_text: str, json_data: Dict, summary_model, mode: str = "lengthen", summary_length: int = 50):
        self.input_text = input_text
        self.json_data = json_data
        self.summary_model = summary_model
        self.mode = mode
        self.summary_length = summary_length

    def find_relevant_keys(self) -> List[str]:
        """Find JSON keys that match the token expressions from the input text."""
        relevant_keys = []
        for key, value in self.json_data.items():
            for expression in value.keys():
                # Use a regular expression to match the expression, even if it's part of a larger word
                if re.search(re.escape(expression), self.input_text, re.IGNORECASE):
                    relevant_keys.append(expression)
        return relevant_keys


    def get_reference_paragraph(self) -> str:
        """Generate a reference paragraph based on the relevant keys."""
        relevant_keys = self.find_relevant_keys()
        paragraph = self.generate_paragraph(relevant_keys)
        return paragraph

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
        # Check if the input paragraph is empty or too short
        if not paragraph or len(paragraph) < 20:
            # Return an appropriate error message or a default summary
            return "Error: The input paragraph is empty or too short."

        try:
            max_position_embeddings = 1024  # This value depends on the model you are using
            min_length = max(10, int(len(paragraph) * 0.1))
            max_length = min(max(512, int(len(paragraph) * 0.3)), max_position_embeddings)
            max_length = max(max_length, min_length)  # Ensure max_length is not smaller than min_length

            # If the input text is too long, truncate it to fit within the model's maximum length
            if len(paragraph) > max_position_embeddings:
                paragraph = paragraph[:max_position_embeddings]

            summary = self.summary_model(paragraph, min_length=min_length, max_length=max_length, do_sample=False)
            return summary[0]["summary_text"]
        except Exception as e:
            log(f"Error generating summary: {e}")
            return f"Error generating summary: {str(e)}"




    def run(self) -> Dict:
        """Run the text processing and summarization."""
        relevant_keys = self.find_relevant_keys()
        paragraph = self.generate_paragraph(relevant_keys)
        summary = self.generate_summary(paragraph)

        result = {
            "input_text": self.input_text,
            "summary": [{"summary_text": summary}],
            "relevant_search_terms": relevant_keys,
            "reference_paragraph": paragraph,
        }

        return result


def main():
    parser = argparse.ArgumentParser(description="Generate a summary based on input text and a JSON file.")
    parser.add_argument("-i", "--input_text", help="Input text provided by the user", default=None)
    parser.add_argument("-p", "--json_path", help="Path to the JSON file", default="PostESG_report.json")
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

