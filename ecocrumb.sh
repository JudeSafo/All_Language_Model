#!/bin/bash

force=0
batch=0
train=0

# Parse command line options
while (( "$#" )); do
  case "$1" in
    --force)
      force=1
      shift
      ;;
    --batch)
      batch=1
      shift
      ;;
    --train)
      train=1
      shift
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done
eval set -- "$PARAMS"

# Check if the user provided the required argument
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "Usage: ./ecocrumb.sh [--force] [--batch] [--train] <target_directory> [num_topics]"
  exit 1
fi

# Define the target directory or directories_path
target=$(realpath $1)

# Define the number of topics (default value: 15)
num_topics=${2:-15}

# If train mode is enabled, run the generate_topics.sh script
if [ "$train" -eq 1 ]; then
  ./esgetlpipeline/src/generate_topics.sh
fi

# If batch mode is enabled, process each folder in the directory
if [ "$batch" -eq 1 ]; then
  for folder in "$target"/*; do
    if [ -d "$folder" ]; then
      echo "Processing folder: $folder"
      if [ "$force" -eq 1 ]; then
        ./ecocrumb.sh --force "$folder" "$num_topics"
      else
        ./ecocrumb.sh "$folder" "$num_topics"
      fi
      echo "Finished processing folder: $folder"
    fi
  done
  exit 0
fi

# Otherwise, process a single target directory
target_directory="$target"

# Define the output directories
topics_features_directory="${target_directory}/topics_features"
parsed_sections_directory="${target_directory}/parsed_sections"

# Create the output directories if they don't exist
mkdir -p "$topics_features_directory"
mkdir -p "$parsed_sections_directory"

# Define the output directory
output_directory=${target_directory}
if [ ! -d $output_directory ]; then
  mkdir $output_directory
fi

# Define the plaintext directory
plaintext_directory="${target_directory}/plaintext"
if [ ! -d $plaintext_directory ]; then
  mkdir $plaintext_directory
fi

# Ensure that the plaintext directory is not the same as the target directory
if [ "$plaintext_directory" = "$target_directory" ]; then
  echo "Error: The plaintext directory and the target directory are the same. Please check your directory structure."
  exit 1
fi

# Count the number of .txt files in the plaintext directory
txt_file_count=$(find "$plaintext_directory" -type f -name "*.txt" | wc -l)

# Convert all PDFs in the target directory to plaintext files only if there are no .txt files
if [ $txt_file_count -eq 0 ]; then
  echo "$(date +'%Y-%m-%d %H:%M:%S') - Converting all PDFs in $target_directory to plaintext files"
  echo "ECHO! - plaintext_directory: $plaintext_directory output_directory: $output_directory"
  # python main.py -i $target_directory -o $plaintext_directory
  ./esgetlpipeline/src/pdf_to_text.sh $target_directory $plaintext_directory
else
  echo "$(date +'%Y-%m-%d %H:%M:%S') - Skipping PDF conversion as .txt files already exist in $plaintext_directory"
fi

echo "Listing .txt files in $plaintext_directory:"
ls "$plaintext_directory"/*.txt
echo

# Process each plaintext file
for file in $plaintext_directory/*.txt; do
  echo "$(date +'%Y-%m-%d %H:%M:%S') - Processing file: $file"
  filename=$(basename $file .txt)

  topics_features_file="${topics_features_directory}/${filename}_topics_features.json"
  parsed_sections_file="${parsed_sections_directory}/${filename}_parsed_sections.json"

  echo "DEBUG: file variable: $file"
  echo "DEBUG: filename variable: $filename"
  echo "DEBUG: output_directory variable: $output_directory"
  echo "DEBUG: output JSON file: ${output_directory}/${filename}_topics_features.json"
  echo "$(date +'%Y-%m-%d %H:%M:%S') - Generating topics_features.json for $filename"

  # Check if the topics_features file already exists
  if [ ! -f "$topics_features_file" ] || [ "$force" -eq 1 ]; then
    # Generate topics_features.json
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Generating topics_features.json for $filename"
    ./esgetlpipeline/src/run_topic_modeling.sh $file 15 "$topics_features_file"
  else
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Skipping topics_features generation for $filename, file already exists"
  fi

  # Check if the parsed_sections file already exists
  if [ ! -f "$parsed_sections_file" ] || [ "$force" -eq 1 ]; then
    # Generate parsed_sections.json
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Generating parsed_sections.json for $filename"
    ./esgetlpipeline/src/parse_by_topic.sh "$file" "$topics_features_file" "$parsed_sections_file"
  else
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Skipping parsed_sections generation for $filename, file already exists"
  fi

done

# Copy contents of parsed_sections to results/ and esg_LanguageModel/src
cp -r "$parsed_sections_directory"/* ./results/
cp -r "$parsed_sections_directory"/* ./esg_LanguageModel/src/
