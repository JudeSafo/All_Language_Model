import re

# Define the keywords to search for
keywords = [
    "Resource Use and Circularity",
    "Product Packaging",
    "Product Design",
    "Supplier ESG Management",
    "Product Health and Safety",
    "Marketing and Labeling",
    "Biodiversity and Land Use",
    "Climate Change Impacts",
    "GHG Emissions",
    "Air Quality",
    "Waste",
    "Water and Wastewater",
    "Diversity, Equity and Inclusion",
    "Human and Labor Rights",
    "Talent Management and Training",
    "Employee Health and Safety",
    "Data Security and Privacy",
    "Food Waste and Security",
    "Community Engagement",
    "Governing Body",
    "Starbucks",
]

# Define the pattern to match the paragraph boundaries
pattern = r"(?:^|\n\n)(.+?)(?:(?=\n\n)|$)"

# Read the document text from a file or other source
with open("../plaintext/Starbucks_Global_Social_Impact_Report.txt", "r") as f:
    text = f.read()

# Loop through each keyword and search for matches in the text
matches = {}
for keyword in keywords:
    regex = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
    for match in regex.finditer(text):
        # Find the full paragraph around the keyword match
        paragraph_match = re.search(pattern, text[0 : match.end()])
        paragraph = paragraph_match.group(1) if paragraph_match else ""

        # Add the paragraph to the matches dictionary
        if keyword not in matches:
            matches[keyword] = []
        matches[keyword].append(paragraph.strip())

# Print the matches for each keyword
for keyword, paragraphs in matches.items():
    print(f'Matches for keyword "{keyword}":')
    for paragraph in paragraphs:
        print(f"  - {paragraph}\n")
