#!/usr/bin/env python3

import os
import argparse
from src.utils import TextAggregator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Aggregate all text files in a directory into a single string."
    )
    parser.add_argument(
        "-i",
        "--input_path",
        type=str,
        help="the path to the input file or the directory containing the text files",
    )
    # parser.add_argument("input_path", help="Directory path or file path to aggregate.")
    args = parser.parse_args()

    text_aggregator = TextAggregator(args.input_path)
    text = text_aggregator.aggregate()
    print(text)

    # Get the directory name as the output file name
    dir_name = os.path.basename(os.path.normpath(args.input_path))
    output_file_name = f"{dir_name}.txt"

    # Get the directory path of the input_path
    input_dir_path = os.path.dirname(os.path.abspath(args.input_path))

    # Create the output file path
    output_file_path = os.path.join(input_dir_path, output_file_name)

    # Save the output to the file
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(text)
