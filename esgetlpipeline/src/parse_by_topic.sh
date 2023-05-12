#!/bin/bash

# Check if the user provided the required arguments
if [ $# -ne 3 ]; then
  echo "$(date +"%Y-%m-%d %H:%M:%S") - ERROR - Usage: ./parse_by_topic.sh <file_name/folder> <topics_features_json_file> <parsed_sections_json_file>"
  exit 1
fi

input_path="$1"
topics_features_json_file="$2"
parsed_sections_json_file="$3"
temp_file="temp.txt"

# Concatenate the plaintext files if the input is a folder
if [ -d "$input_path" ]; then
  echo "$(date +"%Y-%m-%d %H:%M:%S") - INFO - Aggregating text files in $input_path"
  cat "$input_path"/*.txt > "$temp_file"
  input_path="$temp_file"
fi

# Remove carriage returns
tr -d '\r' < "$input_path" > "${input_path}_no_cr.txt"
input_path="${input_path}_no_cr.txt"

# Read the topics and features from topics_features.json
topics_features=$(jq -r 'to_entries | .[] | "\(.key)|\(.value | join("|"))"' "$topics_features_json_file")

# Initialize an empty JSON object
json_result="{}"

# Iterate through the topics and features
while IFS='|' read -ra topic_feature; do
  topic="${topic_feature[0]}"
  features=("${topic_feature[@]:1}")

  # Initialize an empty JSON object for the topic_data
  json_topic="{}"

  # Add the topic to the features
  features=("$topic" "${features[@]}")

  # Iterate through the features
  for feature in "${features[@]}"; do
    # Check if the feature is not equal to the topic
    if [ "$feature" != "$topic" ]; then
      # Extract the sections for the feature using perl
      echo "$(date +"%Y-%m-%d %H:%M:%S") - INFO - Extracting sections for feature: $feature"
      #sections=$(perl -lne "BEGIN {undef $/;} print ((\$& =~ s/\n/ /gr) . '\n') if m/(?<=^|\n|\.|\?)[^\n\.]*\b${feature}\b.*?(?=(\n[^\S\n]*){2,}|\z|\.|\?)/is" "$input_path")
      #sections=$(perl -lne "BEGIN {undef $/;} print ((\$& =~ s/\n/ /gr) . '\n') if m/(^|\n|(?<=\s)[.!?](?:\s+)?)(?=[A-Z])[^\n\.]*\b${feature}\b.*?(?=(\n[^\S\n]*){2,})/is" "$input_path")
      #sections=$(perl -lne "BEGIN {undef $/;} print ((\$& =~ s/\n/ /gr) . '\n') if m/(^|\n|(?<=\s)[.!?](?:\s+)?)(?=[A-Z]|[1-9][.!?]|[1-9][)])[^\n\.]*\b${feature}\b.*?(?=(\n[^\S\n]*){2,})/is" "$input_path")
      sections=$(awk -v feature="${feature}" -v RS='[.!?]+[[:space:]]*' -v ORS='\n' '$0 ~ feature {gsub(/\n/, " "); print}' "$input_path")


      
      
      # Add the sections to a JSON array
      json_sections="[]"
      while read -r section; do       
        # Check if the section is not already in the JSON array and not empty
        if [ "$(echo "$json_sections" | jq --arg section "$section" 'index($section)')" = "null" ] && [ ! -z "$section" ]; then
          # Split the section by bullet points
          IFS='•' read -ra bullet_points <<< "$section"
          first_bullet_point="${bullet_points[0]}"
          first_bullet_point="${first_bullet_point//$'\n'/ }"
          json_sections=$(echo "$json_sections" | jq --arg section "$first_bullet_point" '. + [{"text": $section}]')

          # Add the rest of the bullet points as nested JSON
          for i in "${!bullet_points[@]}"; do
            if [ "$i" -ne 0 ]; then
              bullet_point="${bullet_points[$i]}"
              bullet_point="${bullet_point//$'\n'/ }"
              json_sections=$(echo "$json_sections" | jq --argjson index "$(expr $i - 1)" --arg section "$bullet_point" '.[-1] |= . + {"bp_\($index+1)": $section}')
            fi
          done
        fi
      done <<< "$sections"

      # Add the feature and its sections to the JSON object if the sections are not empty
      if [ "$json_sections" != "[]" ]; then
        json_topic=$(echo "$json_topic" | jq --arg feature "$feature" --argjson sections "$json_sections" '. + {($feature): $sections}')
      fi
    fi
    
  done

  # Add the topic and its features to the JSON object
  json_result=$(echo "$json_result" | jq --arg topic "$topic" --argjson topic_data "$json_topic" '. + {($topic): $topic_data}')
done <<< "$topics_features"

# Remove control characters and unusually long whitespaces
#json_result=$(echo "$json_result" | tr -d '\000-\011\013\014\016-\037' | sed -E 's/(.) {3,}/\1 /g')


# Write the JSON object to a file
echo "$(date +"%Y-%m-%d %H:%M:%S") - INFO - Writing output to $parsed_sections_json_file"
echo "$json_result" > "$parsed_sections_json_file"

# Remove the temporary file if it exists
[ -f "$temp_file" ] && rm "$temp_file"
[ -f "${input_path}" ] && rm "${input_path}"

# Print the JSON object to the console
echo "$(date +"%Y-%m-%d %H:%M:%S") - INFO - JSON Output:"
echo "$json_result"
