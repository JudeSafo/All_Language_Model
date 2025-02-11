[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/569/badge)](https://bestpractices.coreinfrastructure.org/projects/569)<br>

# Ecocrumb - ESG Reporting Handler

To assist with knowledge transfer, as we finalize our work, I've added a Ecocrumb (End-to-End) executable, `ecococrumb`, a command line utility to automate the various aspects of this work: the processing of PDF files to generate topics and parsed sections data, language model training, model hosting and persist changes to api. 
<br><br>The language model (live here http://18.219.52.58:3000/), one of the key deliverables of this work, accepts a user input text in the form of a question or unfinished thought and returns an answer or summary based on relevant material found in the ESG document. 

![Snip20230506_67](https://github.com/JudeSafo/All_Language_Model/assets/9307673/c3fc1d98-042e-4b7b-a8ee-dfe690a4ed41)
The project, spanning just over 1 month (04/05/2023 - 05/05/2023), contains within it many discrete sub-projects. That work is aggregated here for convenience and cogency. The sub-folders, containing work from the various stages of the project, are identified as follows:
1. **_esgreportcrawler_** - used to curate the data needed for the remainder of this project. In total 924 [ESG reports]([url](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false)) were obtained using this crawler, 541 of which are 'food or hotel' related.  ESG reports are almost always pdf files (occasionally .ppt or .pptx). 
2. **_esgetlpipeline_** - Core tooling for processing all of the raw ESG pdf data for downstream tasks.
3. **_esg_language model_** - Core tooling for training, and serving the language model api. These are primarily contained in `llm_esg.py` and `app.py`. Model is hosted via `fastapi` and `uvicorn` on 2 aws ec2 servers (one [production]([url](https://18.219.52.58)), one for [development]([url](https://3.145.190.67))) that are actively running (as of the time of writing this).<br>
The two endpoints for this model are `answer_question` and `generate_summary`:
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
> **Input:** 
> `text` field, containing the user query <br>
> `mode` field, mode dictates whether to 'lengthen' (by concating input to model summary) or 'shorten' (provide relevant summary) of user input. This  is only relevant for the `generate_summary` endpoint <br>
>`json_file` field, provides the pointer to the appropriate json representing the ESG company report in question. This allows the model to hotswap  between different company data without having to store each of them in memory.<br> 
> <br>**Response:**
> the model response in each case is a json containing either an `answer` or `summary` field (depending on the endpoint), a `relevant_search_terms` > field and a `reference_paragraph`.
4. **_esg_webapp_** - A lightweight next.js wrapper for rendering the language model in a user friendly interface (http://18.219.52.58:3000/). 

## Getting Started 

After installation you'll want to process and load data into the language model, then use that to serve the model. 

### Requirements
- macosx/linux os (Debian preferred)
- (optional) aws ec2 VM

### Installation

To install the `ecocrumb` exec:

1. Open a terminal session on your macOS (`cmd` + `space` - search 'terminal') or Linux machine.

2. For the most up to date installation from Haiphen (Jude Safo - pi@haiphenai.com):

   ```bash
   curl -H "Authorization: token YOUR_GITHUB_TOKEN" -o install.sh -sSf https://api.github.com/repos/JudeSafo/All_Language_Model/contents/install.sh | bash
   ```
   or download [here](https://github.com/ecocrumb/All_Language_Model) via github:

   ```git
   git clone https://github.com/ecocrumb/All_Language_Model/ && cd All_Language_Model && ./install.sh 
   ```
   
3. (ven) `source bin/activate` or `pip install -r requirements.txt` the necessary depednencies

### Verify Correct Installation

Verify correct installation:
```bash
ecocrumb --version
v0.0.1
```
inspect documentation

```bash
man ecocrumb
```
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/e5db33b9-6e7b-4156-92b1-093594ae6d21)
_Note_: Installation has been seperately tested and verified on a `macosx` and `debian` os. 

### Basics

Let's process the company `Kellog's` entire ESG report folder and convert this into a machine readable json ending in the suffix _modified_parsed_sections.json_. We will use these jsons to pass as arguments to our language model.

Run the following:
```bash
(etlpipeline) $ ecocrumb --force --batch --train data/ 20
```

here's what each term is doing:

- `data/` this specifies the target company folder or set of company folders to process
- `[20]` optional, this specifies the number of subtopics to associate to each major topic. This number can be as large as you chose.
- `[--force]` optional, overwrite any existing data found in the folder
- `[--batch]` optional, for processing multiple companies at once. Else specify individual company folder (e.g. data/Starbucks)
- `[--train]` option, when adding new `topics`, `subtopics` or `entities` to the `pick_esg_topics.csv` file this flag will persist these changes downstream.

Take a look at the 3 subfolders created during this process `plaintext`, `parsed_sections` and `topic_features`. Inspect the content of each folder and compare with your inputs into the `pick_esg_topics.csv` file. 

You will also see updates to the `results` and `esg_languagemodel/webapp/src` folder. This serves the secondary purpose such that the next time you reload your webapp you will now have access to your newly generated company data.

## Add New Company Data

Copy paste [company folder]([url](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false)) in the `data` directory of this repo. Currently it contains just `Starbucks` and `Kellogs` to start. Full list available on [s3]([url](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false)), [google drive]([url](https://drive.google.com/drive/u/3/folders/1kMDQ8xlPyx4_-JsBc-3DE0OrBDxVOYOc)) and [mongodb]([url](https://cloud.mongodb.com/v2/6437bc8b8cb5a24d728d1cb4#/clusters))
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/170e6e8d-8c65-4340-ade6-da1ff3fe44e1)

### How to improve model behavior by adding additional keywords?

`Topics` are just expressions you want or expect to see in the ESG report of your company (e.g. "supply chain", "child labor", "employee rights"). They are typically 2 words but not limited to this. They span anywhere from 1 - 4 words. We can change the topics set of topics in 1 of two ways: 
1. - Add additional keywords manually to the `pick_esg_topics.csv` file then running the exec in training mode `ecocrumb --train data/Starbucks` as follows
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/ab761efd-30a2-46b4-af4e-3553629c21dd)
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/d0a3cbd0-5e07-4400-8505-2917017b14fa)
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/9dbeb8f4-1d9d-4900-9b20-8656159bff12)

2. - Append the number of topics when invoking `ecocrumb data/Starbucks 10`

The default, if nothing is passed, is 15. The number is a bit misleading because it represents the largest number of subtopics that can be affiliated with a given topic. The subtopics generation are done via `tfidf` ranking as seen in the `esgetlpipeline/src/utils.py` under `TokenTfidfExtractor`. In practice anything more than 30 will show signifcant impact on model performance so experiment for yourself first.

### Serving model
This is largely user preference. 
To test and serve locally you simply need to navigate to `esg_LanguageModel/webapp/src` and run the following:
```python
uvicorn app:app --reload
```
Follow instructions provided by the server for where the api is hosted.<br> 
_Note_:make certain your (venv) is active or you will encounter errors.

### Walk through
https://github.com/JudeSafo/All_Language_Model/assets/9307673/3702b030-5971-4eb6-8541-6fd860849392


### List of AWS architecture
![image](https://github.com/JudeSafo/All_Language_Model/assets/9307673/525107ef-2492-45e0-9551-34e5fedc360f)
(pem key provided seperately for security)

### How to fine tune the model over time?

The content of `esg_LanguageModel` folder outline this all work done around model training. Full model training will require gpu or tpu hardware and additional training data.

## Conclusion

The biggest focus for you short term should be experimenting with keywords and number of topics. In the month spent working on this project I've read through dozens of ESG reports to build my intuition before inspecting the model. As subject matter experts you may not need to do this but there is tremendous value from diving deep into all the material you now have to work with.

Wishing you both the best in your ESG endeavors👋!

Sincerely, Jude Safo<br> 
Haiphen:pi@haiphenai.com 

### Miscellaneous

| Status | Project | Task | Descrip. | Assets | Date |
|--------|---------|------|----------|--------|------|
| ✅ | ESG report entity extraction and report automation | ESG Crawler | Grab raw data | [Github](https://github.com/JudeSafo/All_Language_Model/tree/master/esgreportcrawler), [S3](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false), [mongo](https://cloud.mongodb.com/v2/6437bc8b8cb5a24d728d1cb4#/clusters) | 04/08 |
| ✅ | ESG report entity extraction and report automation | Entity Extraction | Grab entities/topics, parse data | [Github](https://github.com/JudeSafo/All_Language_Model/tree/master/esgetlpipeline), [Mongodb](https://github.com/JudeSafo/All_Language_Model/tree/master/esgetlpipeline) | 04/15 |
| ✅ | ESG report entity extraction and report automation | ETL Pipeline | bash script | [Github](https://github.com/JudeSafo/All_Language_Model/tree/master/esgetlpipeline) | 04/20 |
| ✅ | ESG report entity extraction and report automation | Metrics | Tfidf sorting, llm rankings | [Github](https://github.com/JudeSafo/All_Language_Model/blob/master/esgetlpipeline/src/stats.py) | 05/05 |
| ✅ | ESG report entity extraction and report automation | LLM | lengthen, shorten, summarize | [Github](https://github.com/ecocrumb/esg_LanguageModel), [ec2](https://us-east-2.console.aws.amazon.com/ec2/home?region=us-east-2#InstanceDetails:instanceId=i-0ce9727c6cfdc47e1) | 04/28 |
| ✅ | ESG report entity extraction and report automation | Software Bill of Materials | Full list of software used during this | [Github](https://github.com/JudeSafo/All_Language_Model/blob/master/requirements.txt) | 04/20 |
| ✅ | ESG report entity extraction and report automation | Webapp (Not in original scope) | Interactive webapp | [[Github](https://github.com/JudeSafo/All_Language_Model/tree/master/esg_webapp)], [ec2](http://18.219.52.58:3000/) | 05/05 |
| ✅ | ESG report entity extraction and report automation | Question-Answer Model (Not in original scope) | Secondary ml model | [[Github](https://github.com/JudeSafo/All_Language_Model/tree/master/esg_LanguageModel)], [ec2](http://18.219.52.58:3000/) | 05/05 |
| ✅ | ESG report entity extraction and report automation | Automation handler (Not in original scope) | bash exec automate various components of project | [Github](https://github.com/JudeSafo/All_Language_Model) | 05/12 |

#### Fun Stats
Code Base<br>
> Total lines of code - 1,786,759<br>
> Word Count - 11,659,299<br>
> Hours commited - > 500 hours<br>

Reports<br>
> ESG Report count - 924 (541 food & hotel companies, 383 others)<br>
> ESG Company count - 249 (129 food & hotel; 120 others)<br>
> ESG Page count - on average 25 - 50 pages (max 110)<br>



