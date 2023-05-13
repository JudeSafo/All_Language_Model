[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/569/badge)](https://bestpractices.coreinfrastructure.org/projects/569)<br>

# Ecocrumb - ESG Reporting Handler

The Ecocrumb (End-to-End) script is a utility script that automates the processing of PDF files to generate topics and parsed sections data. It utilizes other supporting scripts such as `pdf_to_text.sh`, `run_topic_modeling.sh`, and `parse_by_topic.sh`.

# Getting Started 

This repository contains all of the components

## Requirements
- macosx
- linux os (debian preferred0
- aws ec2 virtual machine

## Installation

To install the `ecocrumb` exec:

1. Open a terminal session on your macOS (cmd + space - terminal) or Linux machine.

2. For the most up to date installation from Haiphen (Jude Safo - pi@haiphenia.com):

   ```bash
   curl -H "Authorization: token YOUR_GITHUB_TOKEN" -o install.sh -sSf https://api.github.com/repos/JudeSafo/All_Language_Model/contents/install.sh | bash
   ```
   or download [here](https://github.com/ecocrumb/esg_deliverables) via github:

   ```git
   git clone https://github.com/ecocrumb/esg_deliverables/ && cd esg_deliverables && ./install.sh 
   ```
   
3. (ven) `source bin/activate` or `pip install -r requirements.txt` the necessary depednencies

## Verify Correct Installation

Verify correct installation via:
```bash
ecocrumb --version
v0.0.1
```
and verify documentation

```bash
man ecocrumb
```
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/13cceaaf-8bba-4132-a45d-5ffae7e42f0b)
Note: Installation has been seperately tested and verified on a `macosx` and `debian` os.

# Add New Company Data

Copy paste [company folder]([url](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false)) in the `data` directory of this repo. Currently it contains just `Starbucks` and `Kellogs` to start. Full list available on s3, [google drive](url) and [mongodb]([url](https://cloud.mongodb.com/v2/6437bc8b8cb5a24d728d1cb4#/clusters))

## Define Topics

