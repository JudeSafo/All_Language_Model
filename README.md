[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/569/badge)](https://bestpractices.coreinfrastructure.org/projects/569)<br>

# Ecocrumb - ESG Reporting Handler

The Ecocrumb (End-to-End) executable, `ecococrumb` is a command line utility to automate the various aspects of this work: the processing of PDF files to generate topics and parsed sections data and eventually train a language model. ESG reports are almost always pdf files (rarely .ppt or .pptx). 

![Snip20230506_67](https://github.com/JudeSafo/All_Language_Model/assets/9307673/c3fc1d98-042e-4b7b-a8ee-dfe690a4ed41)
The folders contain work from the various stages of the project are summarized as follows:
1. **_esgreportcrawler_** - used to curate the data used for the remainder of this work. In total 924 [ESG reports]([url](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false)) were crawled, 541 of which are 'food or hotel' related
2. **_esgetlpipeline_** - Core tooling for processing all of the raw ESG pdf data for downstream tasks.
3. **_esg_language model_** - Core tooling for training, and serving the language model api. These are primarily contained in `llm_esg.py` and `app.py`. Model is hosted via `fastapi` and `uvicorn` on 2 aws ec2 servers (one [production]([url](https://18.219.52.58)), one for [development]([url](https://3.145.190.67))) that are actively running (as of the time of writing this). The two endpoints for this model are `answer_question` and `generate_summary`:
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{
    "text": "Kraft Heinz approach to efficiency projects?",
    "mode": "lengthen",
    "json_file": "KraftHeinz-2022-ESG-Report_parsed_sections.json"
}' http://3.133.103.207/generate_summary

$ curl -X POST -H "Content-Type: application/json" -d '{
    "text": "Kraft Heinz approach to efficiency projects?",
    "mode": "lengthen",
    "json_file": "KraftHeinz-2022-ESG-Report_parsed_sections.json"
}' http://3.133.103.207/answer_question
```
4. **_esg_webapp_** - A lightweight next.js wrapper for rendering the language model in a user friendly interface. 

# Getting Started 

After installation we'll start off we'll process and load data into the language model, then focus on serving and training. The webapp is provided as is.

## Requirements
- macosx
- linux os (Debian preferred)
- aws ec2 virtual machine

## Installation

To install the `ecocrumb` exec:

1. Open a terminal session on your macOS (cmd + space - search 'terminal') or Linux machine.

2. For the most up to date installation from Haiphen (Jude Safo - pi@haiphenia.com):

   ```bash
   curl -H "Authorization: token YOUR_GITHUB_TOKEN" -o install.sh -sSf https://api.github.com/repos/JudeSafo/All_Language_Model/contents/install.sh | bash
   ```
   or download [here](https://github.com/ecocrumb/All_Language_Model) via github:

   ```git
   git clone https://github.com/ecocrumb/All_Language_Model/ && cd All_Language_Model && ./install.sh 
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
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/e5db33b9-6e7b-4156-92b1-093594ae6d21)
Note: Installation has been seperately tested and verified on a `macosx` and `debian` os.

## Basics

Let's process the company `Kellog's` entire ESG report folder and convert this into a machine readable json ending in the suffix _modified_parsed_sections.json_. We will use these jsons to pass as arguments to our language model.

Run the following:
```bash
(etlpipeline) $ ecocrumb --force --batch --train data/ 20
```

here's what each term is doing:
- `[--force]` optional, overwrite any existing data found in the folder
- `[--batch]` optional, for processing multiple companies at once. Else specify individual company folder (e.g. data/Starbucks)
- `[--train]` option, when adding new `topics`, `subtopics` or `entities` to the `pick_esg_topics.csv` file this flag will persist these changes.
- `data/` this specify the target company folder or set of company folders to process
- `20`, this specifies the number of subtopics to associate to each major topic. This number can be as large as you chose.

Take a look at the 3 subfolders created during this process `plaintext`, `parsed_sections` and `topic_features`. Inspect the content of each folder and compare with your inputs into the `pick_esg_topics.csv` file. 

You will also see updates to the `results` and `esg_languagemodel/webapp/src` folder. This serves the secondary purpose such that the next time you reload your webapp you will now have access to your newly generated company data.

# Add New Company Data

Copy paste [company folder]([url](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false)) in the `data` directory of this repo. Currently it contains just `Starbucks` and `Kellogs` to start. Full list available on [s3]([url](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false)), [google drive]([url](https://drive.google.com/drive/u/3/folders/1kMDQ8xlPyx4_-JsBc-3DE0OrBDxVOYOc)) and [mongodb]([url](https://cloud.mongodb.com/v2/6437bc8b8cb5a24d728d1cb4#/clusters))
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/170e6e8d-8c65-4340-ade6-da1ff3fe44e1)

## How to improve model behavior by adding additional keywords?

`Topics` are just expressions you want or expect to see in the ESG report of your company (e.g. "supply chain", "child labor", "employee rights"). They are typically 2 words but not limited to this. They span anywhere from 1 - 4 words. We can change the topics set of topics in 1 of two ways: 
1. - Add additional keywords manually to the `pick_esg_topics.csv` file then running the exec in training mode `ecocrumb --train data/Starbucks` as follows
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/afe1f1f8-d4fd-4d75-b339-95a2a407fc38)
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/d0a3cbd0-5e07-4400-8505-2917017b14fa)
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/9dbeb8f4-1d9d-4900-9b20-8656159bff12)

2. - Append the number of topics when invoking `ecocrumb data/Starbucks 10`
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/535253c2-6170-433f-8b5e-f54bd8c94108)

The default is set to 15. The number is a bit misleading because it the largest number of subtopics that can be affiliated with a given topic. The subtopics generation are done via `tfidf` ranking as seen in the `esgetlpipeline/src/utils.py` under TokenTfidfExtractor. In practice anything more than 30 will show signifcant impact on model performance so experiment for yourself first.

## List of AWS architecture
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/525107ef-2492-45e0-9551-34e5fedc360f)
(pem key provided seperately for security)

## How to fine tune the model over time?

The content of esg_LanguageModel folder outline this all work done around model training. Proper fine tuning will gpu or tpu hard drive and additional question/user responses.


