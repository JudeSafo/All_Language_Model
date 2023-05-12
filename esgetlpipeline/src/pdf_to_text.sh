#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
  echo "Usage: pdf_to_text.sh <input_file_or_folder> <output_folder>"
  exit 1
fi

# Assign input and output paths
input_path="$1"
output_folder="$2"

# Create the output folder if it doesn't exist
mkdir -p "$output_folder"

# Function to convert a single PDF file to a text file
function convert_pdf_to_text() {
  pdf_file="$1"
  output_text_file="$2"

  # Convert the PDF to text using pdftotext, suppressing warnings
  pdftotext -layout "$pdf_file" "$output_text_file" 2>/dev/null

  echo "Converted $pdf_file to $output_text_file"
}

# Function to call the process_plaintext.py script
function process_plaintext() {
  input_text_file="$1"
  output_modified_text_file="$2"

  python3 esgetlpipeline/src/process_plaintext.py "$input_text_file" "$output_modified_text_file"
}

# Check if the input is a file or a folder
if [ -f "$input_path" ]; then
  # Input is a single file
  base_file_name=$(basename "$input_path" .pdf)
  output_text_file="$output_folder/$base_file_name.txt"

  convert_pdf_to_text "$input_path" "$output_text_file"
  process_plaintext "$output_text_file" "$output_folder/${base_file_name}_modified.txt"
  rm "$output_text_file"
elif [ -d "$input_path" ]; then
  # Input is a folder
  for pdf_file in "$input_path"/*.pdf; do
    base_file_name=$(basename "$pdf_file" .pdf)
    output_text_file="$output_folder/$base_file_name.txt"

    convert_pdf_to_text "$pdf_file" "$output_text_file"
    process_plaintext "$output_text_file" "$output_folder/${base_file_name}_modified.txt"
    rm "$output_text_file"
  done
else
  echo "Invalid input path. Please provide a valid file or folder."
  exit 1
fi
