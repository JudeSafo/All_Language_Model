#!/bin/bash

# Read the CSV file, skip the header, and create the topics.txt file
awk -F, 'NR > 1 {
  if ($1 != "") {
    topic=$1;
    subtopics=$2;
  } else {
    subtopics=subtopics ", " $2;
  }
  if ($3 != "") {
    subtopics=subtopics ", " $3;
  }
  print topic ":" subtopics;
}' topics.csv > topics.txt

