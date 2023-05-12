import os
import re
import json
import sys
from pathlib import Path


def extract_sections(file_path, features, min_length=50):
    with open(file_path, "r") as file:
        text = file.read()

    sections = []
    for feature in features:
        pattern = re.compile(r"(\b" + re.escape(feature) + r"\b.*?\.)", re.IGNORECASE)
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) >= min_length:
                sections.append(match.strip())

    return sections


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_by_topic.py <file_name/folder>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_file = "parsed_sections.json"

    with open("topics_features.json", "r") as file:
        topic_features = json.load(file)

    aggregated_text = ""
    if os.path.isfile(input_path):
        aggregated_text = Path(input_path).read_text()
    elif os.path.isdir(input_path):
        for file in os.listdir(input_path):
            file_path = os.path.join(input_path, file)
            if os.path.isfile(file_path) and file_path.endswith(".txt"):
                aggregated_text += Path(file_path).read_text()

    topic_sections = {}
    for topic, features in topic_features.items():
        sections = extract_sections(input_path, features)
        topic_sections[topic] = sections

    with open(output_file, "w") as file:
        json.dump(topic_sections, file, indent=2)

    print(f"Output saved to {output_file}")
