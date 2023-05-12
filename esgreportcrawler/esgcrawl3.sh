#!/bin/bash

#Copyright © 2023, Soulworks Technologies
#Author: Jude Safo
#Date: 03/05/2023
#Description: 

# Set the location of the CSV file
CSV_FILE="companies.csv"
OUTPUT_DIR="reports" # Set the output directory
DELAY=180  # Set the delay between queries in seconds
LOG_FILE="query.log"  # Set the log file

# Define additional intitle fields
ADDITIONAL_INTITLE="(Sustainability reporting|Corporate responsibility reporting|Environmental reporting|Social reporting|Governance reporting|Responsible investing|Ethical investing|Green investing|ESG disclosure|ESG performance|ESG metrics|ESG ratings|ESG analysis|ESG integration|ESG criteria|ESG|CSR|Sustainability|Impact Report|responsibility report)"

# Function to search for subdomains and download matching files
function search_subdomains {
  local DOMAIN=$1
  local QUERY="site:$DOMAIN ext:pdf OR ext:pptx intitle:ESG OR intitle:CSR OR intitle:Sustainability OR intitle:\"Impact Report\" OR intitle:\"responsibility report\""
  local QUERY_ENCODED=$(echo "$QUERY" | sed 's/ /%20/g')
  local URL="https://www.google.com/search?q=$QUERY_ENCODED"

  # Use lynx to simulate a browser and save the HTML output
  local HTML=$(lynx -useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" -dump "$URL")

  # Loop through each link in the HTML output
  while read -r LINK; do

    # Check if the link matches the specified file types and keywords
    if echo "$LINK" | grep -qE 'https://.*\.(pdf|pptx|ppt).*($ADDITIONAL_INTITLE)'; then

      # Construct the file name from the link
      local FILENAME=$(echo "$LINK" | sed -e 's/https:\/\///' -e 's/\//_/g')

      # Use curl to download the file and save it to the output directory
      curl -sS -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" -o "$COMPANY_DIR/$FILENAME" "$LINK"

      # Wait for the specified delay before performing the next query
      sleep "$DELAY"

    fi

  done < <(echo "$HTML" | grep -o 'https://[^"]*\.pdf\|https://[^"]*\.pptx\|https://[^"]*\.ppt')

  # Log the query
  echo "Query for $DOMAIN completed on $(date)" >> "$LOG_FILE"
}

# Loop through each line in the CSV file
tail -n +2 "$CSV_FILE" | while read -r NAME DOMAIN; do
  # Process company name using regex
  SANITIZED_NAME=$(echo "$NAME" | sed 's/[^a-zA-Z0-9_-]//g')

  # Create the output directory for this company
  COMPANY_DIR="$OUTPUT_DIR/$SANITIZED_NAME"
  mkdir -p "$COMPANY_DIR"

  # Construct the Google Dork query for this company's domain and encodes it for use in the URL
  QUERY="site:$DOMAIN ext:pdf OR ext:pptx OR ext:ppt intitle:$ADDITIONAL_INTITLE"
  QUERY_ENCODED=$(echo "$QUERY" | sed 's/ /%20/g')
  URL="https://www.google.com/search?q=$QUERY_ENCODED"

  # Use lynx to simulate a browser and save the HTML output
  HTML=$(lynx -useragent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36" -accept_all_cookies -dump "$URL")
 

  # Loop through each link in the HTML output
  while read -r LINK; do

    # Check if the link matches the specified file types and keywords
    if echo "$LINK" | grep -qE "https://.*\.(pdf|pptx|ppt).*($ADDITIONAL_INTITLE)"; then

    # Invoke the dfs_search function for each link
      while read -r DFS_LINK; do

        # Construct the file name from the link
        FILENAME=$(echo "$DFS_LINK" | sed -e 's/https:\/\///' -e 's/\//_/g')

        # Use curl to download the file and save it to the output directory
        curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" -o "$COMPANY_DIR/$FILENAME" "$DFS_LINK"

        # Wait for the specified delay before performing the next query
        sleep "$DELAY"

      done < <(search_subdomains "$DOMAIN" "$LINK")

    fi

  done < <(echo "$HTML" | grep -oE 'https://[^"]*\.(pdf|pptx|ppt)')

    # Write metadata to a YAML file
  echo "name: $NAME" > "$COMPANY_DIR/$SANITIZED_NAME.yaml"
  echo "domain: $DOMAIN" >> "$COMPANY_DIR/$SANITIZED_NAME.yaml"
  echo "query: $QUERY" >> "$COMPANY_DIR/$SANITIZED_NAME.yaml"
  echo "HTML: $HTML" >> "$COMPANY_DIR/$SANITIZED_NAME.yaml"
  echo "URL: $URL" >> "$COMPANY_DIR/$SANITIZED_NAME.yaml"
  echo "timestamp: $(date +%Y-%m-%d\ %H:%M:%S)" >> "$COMPANY_DIR/$SANITIZED_NAME.yaml"

  # Log the query
  echo "Query for $NAME $DOMAIN $QUERY $(head -5 "$HTML") $URL completed on $(date +"%Y-%m-%d %H:%M:%S")" >> "$LOG_FILE"

done < "$CSV_FILE"
