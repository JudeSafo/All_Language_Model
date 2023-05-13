[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/569/badge)](https://bestpractices.coreinfrastructure.org/projects/569)<br>

# Ecocrumb - ESG Reporting Handler

The Ecocrumb (End-to-End) executable, `ecococrumb` is a command line utility to automate the various aspects of this work. the processing of PDF files to generate topics and parsed sections data. ESG reports are almost always pdf files (rarely .ppt or .pptx). The work contained in the various folders can be summarized as follows:
1. _esgreportcrawler_ - used to curate the data used for the remainder of this work. In total 924 [ESG reports]([url](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false)) were crawled, 541 of which are good company related

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
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/af74ffad-238e-44ee-92dc-4b2ccabd06de)
Note: Installation has been seperately tested and verified on a `macosx` and `debian` os.

## Basics

Let's process the company `Kellog's` entire ESG report folder and convert this into a machine readable json ending in the suffix _modified_parsed_sections.json_
We will use these jsons to pass as arguments to our language model.

# Add New Company Data

Copy paste [company folder]([url](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false)) in the `data` directory of this repo. Currently it contains just `Starbucks` and `Kellogs` to start. Full list available on s3, [google drive](url) and [mongodb]([url](https://cloud.mongodb.com/v2/6437bc8b8cb5a24d728d1cb4#/clusters))
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/f5249fc9-e1aa-4885-ace6-c480c8933e8f)

## Define/Add Topics

`Topics` are just expressions you want or expect to see in the ESG report of your company (e.g. "supply chain", "child labor", "employee rights"). They are typically 2 words but not limited to this. They span anywhere from 1 - 4 words. We can change the topics set of topics in 1 of two ways: 
1. - Add additional keywords manually to the `pick_esg_topics.csv` file then running the exec in training mode `ecocrumb --train data/Starbucks` as follows
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/9d263535-da99-4d33-8a2e-18006d89c8c2)
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/25939a33-dba9-4151-8f37-030a643f5290)
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/d0a3cbd0-5e07-4400-8505-2917017b14fa)
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/9dbeb8f4-1d9d-4900-9b20-8656159bff12)

2. - Append the number of topics when invoking `ecocrumb data/Starbucks 10`
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/535253c2-6170-433f-8b5e-f54bd8c94108)

The default is set to 15. The number is a bit misleading because it the largest number of subtopics that can be affiliated with a given topic. The subtopics generation are done via `tfidf` ranking as seen in the `esgetlpipeline/src/utils.py` under TokenTfidfExtractor. In practice anything more than 30 will show signifcant impact on model performance so experiment for yourself first.

