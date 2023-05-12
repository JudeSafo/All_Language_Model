#!/bin/env python3

import re
import json
import sys

if len(sys.argv) != 3:
    print("Usage: python3 section_headers.py <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]
headers_file = "headers.txt"
output_file = sys.argv[2]

# Initialize output dictionary
output_dict = {}

with open(input_file, "r") as f:
    input_data = f.read()

with open(headers_file, "r") as f:
    headers_data = f.read().splitlines()

for i in range(len(headers_data) - 1):
    header = headers_data[i]
    print(f"Processing header: {header}")

    # Find the section of text immediately following the header
    pattern = re.compile(rf"{header}\s*([\s\S]*?)(?=\n{headers_data[i+1]}|$)", re.IGNORECASE)
    match = pattern.search(input_data)

    if match:
        # Sanitize the header to remove special characters
        sanitized_header = re.sub(r"[^a-zA-Z0-9\s]", "", header)

        # Extract the content and remove escape sequences
        content = match.group(1).strip().replace('\n', '').replace('\r', '').replace('\t', '').encode('ascii', 'ignore').decode('ascii')

        # Add the extracted content to the output dictionary
        output_dict[sanitized_header] = content

        print(f"Extracted content for header '{header}': {content}")
    else:
        print(f"Error: Header not found in the input document: {header}", file=sys.stderr)

# Process the last header separately
header = headers_data[-1]
print(f"Processing header: {header}")

# Find the section of text immediately following the header
pattern = re.compile(rf"{header}\s*([\s\S]*?)$", re.IGNORECASE)
match = pattern.search(input_data)

if match:
    # Sanitize the header to remove special characters
    sanitized_header = re.sub(r"[^a-zA-Z0-9\s]", "", header)

    # Extract the content and remove escape sequences
    content = match.group(1).strip().replace('\n', '').replace('\r', '').replace('\t', '').encode('ascii', 'ignore').decode('ascii')

    # Add the extracted content to the output dictionary
    output_dict[sanitized_header] = content

    print(f"Extracted content for header '{header}': {content}")
else:
    print(f"Error: Header not found in the input document: {header}", file=sys.stderr)

# Write the output dictionary to the output file
with open(output_file, "w") as f:
    json.dump(output_dict, f, indent=2)

print(f"Finished processing headers. JSON output saved to {output_file}.")

