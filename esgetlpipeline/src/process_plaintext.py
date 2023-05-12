import sys
import re
from collections import Counter


def detect_column_boundaries(lines):
    whitespace_counts = Counter()

    for line in lines:
        spaces = re.findall(r' {2,}', line)
        for space in spaces:
            count = len(space)
            whitespace_counts[count] += 1

    common_counts = whitespace_counts.most_common(5)
    column_boundaries = [count for count, _ in common_counts]
    column_boundaries.sort()
    return column_boundaries


def join_columns(line, column_boundaries):
    column_positions = []
    for boundary in column_boundaries:
        space = " " * boundary
        if space in line:
            column_positions.append(line.index(space))
    column_positions.sort()

    chunks = []
    start = 0
    for pos in column_positions:
        chunks.append(line[start:pos].strip())
        start = pos + column_boundaries[-1]
    chunks.append(line[start:].strip())

    return chunks


def process_file(input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    column_boundaries = detect_column_boundaries(lines)

    modified_lines = []
    current_sections = []

    page_delimiter_pattern = r".*- Annual Report \d{4} \d+|Post Holdings, Inc\."
    camel_case_pattern = r"^[A-Z][a-z]+(\s?[A-Z][a-z]+)+\s{2,}|^\s*$"

    for line in lines:
        if re.search(page_delimiter_pattern, line):
            continue

        if re.match(camel_case_pattern, line.strip()):
            if any(current_sections):
                modified_lines.extend(s.strip() for s in current_sections if s.strip())
                current_sections = []

            modified_lines.append(line.strip())
        else:
            chunks = join_columns(line, column_boundaries)
            if len(chunks) > len(current_sections):
                current_sections.extend([""] * (len(chunks) - len(current_sections)))

            for i, chunk in enumerate(chunks):
                if chunk:
                    if current_sections[i] and current_sections[i][-1] != " ":
                        current_sections[i] += " "
                    current_sections[i] += chunk

    if any(current_sections):
        modified_lines.extend(s.strip() for s in current_sections if s.strip())

    with open(output_file, "w") as f:
        f.write("\n".join(modified_lines))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_plaintext.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_file(input_file, output_file)
