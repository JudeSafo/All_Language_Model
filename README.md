[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/569/badge)](https://bestpractices.coreinfrastructure.org/projects/569)<br>

# Ecocrumb - ESG Reporting Handler

The Ecocrumb (End-to-End) script is a utility script that automates the processing of PDF files to generate topics and parsed sections data. It utilizes other supporting scripts such as `pdf_to_text.sh`, `run_topic_modeling.sh`, and `parse_by_topic.sh`.

# Getting Started with All_Language_Model

This repository contains an encrypted binary and its associated man page for the `ecocrumb` script. Follow the instructions below to get started and install the necessary components on macOS or Linux machines.

## Installation

To install the `ecocrumb` exec, simply:

1. Open Terminal on your macOS or Linux machine.

2. For the most up to date installation from Haiphen (pi@haiphenia.com):

   ```bash
   curl -H "Authorization: token YOUR_GITHUB_TOKEN" -o install.sh -sSf https://api.github.com/repos/JudeSafo/All_Language_Model/contents/install.sh | bash

   ```
   or download via current repo

   ```git
   git clone https://github.com/ecocrumb/esg_deliverables/ && cd esg_deliverables && ./install.sh 

## Basics

Verify correct installation via:
```bash
ecocrumb --version

```
