#!/bin/bash

cp choose_esg_topics.csv esgetlpipeline/src/topics.csv
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
}' esgetlpipeline/src/topics.csv > esgetlpipeline/src/topics.txt

