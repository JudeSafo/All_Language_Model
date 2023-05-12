#!/bin/bash

# Check if the user provided the required argument
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "Usage: ./batch_e2e.sh <directories_path> [num_topics]"
  exit 1
fi

# Define the directories_path
directories_path=$(realpath $1)

# Define the number of topics (default value: 15)
num_topics=${2:-15}

# Iterate through each folder in the directory and run e2e.sh
for folder in "$directories_path"/*; do
  if [ -d "$folder" ]; then
    echo "Processing folder: $folder"
    ./e2e.sh "$folder" "$num_topics"
    echo "Finished processing folder: $folder"
  fi
done