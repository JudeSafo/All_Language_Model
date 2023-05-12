#!/bin/bash
#topics=("Resource Use and Circularity" "Product Packaging" "Product Design" "Supplier ESG Management" "Product Health and Safety" "Marketing and Labeling" "Biodiversity and Land Use" "Climate Change Impacts" "GHG Emissions" "Air Quality" "Waste" "Water and Wastewater" "Diversity, Equity and Inclusion" "Human and Labor Rights" "Talent Management and Training" "Employee Health and Safety" "Data Security and Privacy" "Food Waste and Security" "Community Engagement" "Governing Body" "ESG Oversight" "Ethics and Compliance" "Economic Contribution" "Tax Transparency" "Value of Sustainable Innovation")

# Check if the user provided the required arguments
if [ "$#" -ne 2 ] && [ "$#" -ne 3 ]; then
  echo "Usage: ./run_topic_modeling.sh <file_name/folder> <number_of_features> [output_json_file]"
  exit 1
fi

# Define the output JSON file path
if [ "$#" -eq 3 ]; then
  output_json_file=$3
else
  output_json_file="topics_features.json"
fi

# Define the input file/folder and number of features
input=$1
num_features=$2

# Check if the input is a file or a directory
if [ -d "$input" ]; then
  # Create a temporary file to store the aggregated text
  tmp_file=$(mktemp)
  echo "$(date +'%Y-%m-%d %H:%M:%S') - INFO - Temporary file path: $tmp_file"

  # Concatenate all text files in the directory
  find "$input" -type f -iname '*.txt' -exec cat {} + > "$tmp_file"

  # Update the input variable to point to the temporary file
  input="$tmp_file"
  echo "$(date +'%Y-%m-%d %H:%M:%S') - INFO - Processing folder, aggregated file: $input"
elif [ -f "$input" ]; then
  echo "$(date +'%Y-%m-%d %H:%M:%S') - INFO - Processing single file: $input"
else
  echo "$(date +'%Y-%m-%d %H:%M:%S') - ERROR - Invalid input, please provide a file or a folder"
  exit 1
fi

# Read the topics.txt file
IFS=$'\n' read -d '' -ra topics < esgetlpipeline/src/topic_models/topics.txt

# Initialize an empty JSON object
json_result="{}"

# Iterate through the list of topics and run the Python script
for topic_line in "${topics[@]}"; do
  # Split the line into topic and value
  IFS=: read -r topic value <<< "$topic_line"

  echo "$(date +'%Y-%m-%d %H:%M:%S') - INFO - Processing topic: $topic"

  # Run the Python script and save the output to a variable
  output=$(python esgetlpipeline/src/token_similarity.py -i "$input" -n "$num_features" -t "$topic $value")

  # Extract the features from the output and format them as a JSON array
  features=$(echo "$output" | perl -lne 'print $1 if /^(.*?): \d+\.\d+%$/' | jq -R . | jq -s .)

  # Add the topic and features to the JSON object
  json_result=$(echo "$json_result" | jq --arg topic "$topic" --argjson features "$features" '. + {($topic): $features}')
done

# Write the JSON object to a file
echo "$json_result" > "$output_json_file"

# Print the JSON object to the console
echo "$json_result"

# Remove the temporary file if it was created
if [ -f "$tmp_file" ]; then
  rm "$tmp_file"
fi

