import csv
import re
import json

# Hardcode initial tokens
tokens = ["GHG", "Waste", "Biodiversity", "Supply Chain", "Starbucks"]
pattern = r"\b(?:{})\b".format("|".join(tokens))

# Initialize a dictionary to store the results
results = {}

# Open the text file and read the contents
script_dir = os.path.dirname(os.path.abspath(__file__))
data = os.path.join(
    script_dir, "..", "plaintext/Starbucks_Global_Social_Impact_Report.txt"
)
with open(data) as textfile:
    text = textfile.read()

# Split the text into sentences
# sentences = re.split('[.!?]', text)
sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)

# Loop through each sentence and check if it contains a token
for sentence in sentences:
    matches = re.findall(pattern, sentence)
    if re.search(token, sentence):
        # Add the token key to the dictionary if it doesn't already exist
        results.setdefault(token, []).append(sentence.strip())

# Write the results to a JSON file
with open("../results/results.json", "w") as jsonfile:
    json.dump(results, jsonfile)
