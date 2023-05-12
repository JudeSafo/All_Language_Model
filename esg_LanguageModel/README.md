# ESG LLM - Summarize ESG Report Data

[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/569/badge)](https://bestpractices.coreinfrastructure.org/projects/569)<br>

## Purpose

The ESG Language Model (e-LLM) is designed to fine-tune a pre-trained language model for summarization of `esg specific report data` with the ability to `lengthen` or `shorten` the generated summary based on specific requirements.
<div align="center">
  <img src="demo/demo.gif" alt="Demo GIF">
</div>

It's called as follows:
```bash
(llm) $ python llm_esg.py -i "Post Consumer Brands believes that one way to make the world a
better place is by continuously improving packaging ..." -p ESG_report.json
```

with the option to pass the users `input_text` as an argument or get prompted for it at run time. Here the `ESG_report.json` contains the sections of the esg report that will be used for summarization. 

Here's the corresponding of the **[output](results/output.json)** (see `results` folder):
```bash
{
  "input_text": " Post Consumer Brand is committed to sustainability and delivering a positive impact on the world. This year we have refreshed our strategic framework to align with our purpose. Our purpose is to connect people and the community through food. packaging material ...",
  "summary": [
    {
      "summary_text": " Post is committed to partnering with the best suppliers and is an advocate of supplier diversity . 90% of supplier facilities providing ingredients and packaging materials are located domestically in North America or Europe . The company reduced paper packaging material usage by about 930,000 pounds last year ."
    }
  ],
  "relevant_search_terms": [
    "packaging material",
  ],
  "reference_paragraph": "Business Relevance   Our businesses rely on steady supplies of ingredients and packaging materials to be used in products, which are purchased directly from approximately 2,300 domestic and international supplier facilities Given our company\u2019s operational footprint, approximately 90% of supplier facilities providing ingredients and packaging materials are located domestically in North America or Europe In fiscal year 2022, Post companies procured ingredients and packaging materials directly from approximately 2,300 supplier facilities with geographical breakdown as shown to the right:   Ingredient and Packaging Procurement by Region North America 75 % Europe 13% Rest of the world 12%     SUPPLIER DIVERSITY     Post is committed to partnering with the best suppliers and is an advocate of supplier diversity, believing it brings strength and flexibility to our supply base and increases competition in the sourcing process Plastic isn\u2019t the only packaging material we\u2019re working to reduce our usage of Last year, we reduced paper packaging material usage by about 930,000 pounds Currently, about 90% of the packaging materials, by weight, that Post Consumer Brands uses in manufacturing plants are made from recycled content or renewable resources and can be recycled by consumers The year before, the Post Consumer Brands team reduced paper packaging material usage by about 930,000 pounds "
}
```
**Summarize**: `summary_text` is the argument returned to the user if they request for their input query be shortened<br>
**Extend**: `input_text` + `summary_text` are concatenated together in the event the user wants a longer summary (length tbf)
`aggreggated_paragraph` are the subsections pulled from the `ESG_report.json` to generate the the summary. This way the user always has a way to diagnose and assess the veracity of a summary given to them. This will not be returned to the user but rather is only provided for debugging purposes. 

## Features

- Extracts relevant information from a JSON file based on user-supplied expressions
- Aggregates the extracted information into a paragraph
- Generates a concise summary of the aggregated paragraph using the Hugging Face transformers library
- Handles edge cases, such as duplicate paragraphs and token count limits

## Requirements

- Python 3.6 or higher
- Hugging Face transformers library (tested with version 4.13.0)
- tqdm library (tested with version 4.62.3)

To install the required libraries, run:
### Prerequisites

- Python 3.x
- transformers
- torch
- datasets
- (Optional) An AWS EC2 instance with a deep learning AMI, preferably with GPU support (e.g., p2.xlarge or p3.xlarge) for large-scale training.

(see requirements document for full list)
![image](https://user-images.githubusercontent.com/9307673/235316469-c6970297-0798-49c9-82ba-e4781bd0c2da.png)
### Training Model
1.
Prepare your dataset according to the schema mentioned in the project documentation. The dataset should contain `input_text`, `output_text_short`, and `output_text_long` fields.
2. 
Fine-tune the pre-trained model using the provided training script:
```python
python train.py --model model-name --train_file path-to-train-file --validation_file path-to-validation-file --epochs number-of-epochs --output_dir path-to-output-directory
```
3. Generate summaries using the fine-tuned model

```python
python llm_esg.py --model path-to-fine-tuned-model -i `input_text` -p path-to-ESG_reprort-json --summary_type short|long
```
### Models
This project supports fine-tuning the following pre-trained models for summarization tasks:

1. DistilBART: A smaller, faster version of BART that performs well on summarization tasks.
2. T5: A text-to-text model that demonstrates strong performance across various NLP tasks, including summarization.
3. PEGASUS: A model specifically designed for abstractive summarization tasks.

### Code Breakdown
`**TextProcessor class**`: The main class that handles the entire process, from reading the JSON file to generating the summary.
__init__: Initializes the class with the JSON file path and the list of expressions to match.
- _read_json_file_: Reads the JSON file and stores its content in the json_data attribute.
- _find_relevant_keys_: Finds the keys in the JSON data whose values match the given expressions.
- _generate_paragraph_: Creates a paragraph based on the values corresponding to the matched keys.
- _generate_summary_: Generates a summary of the aggregated paragraph using the Hugging Face transformers library.
- _generate_: Main method that combines all the steps to generate the summary.


### Notes
The script currently uses the sshleifer/distilbart-cnn-12-6 model from Hugging Face with the revision a4f8f3e for text summarization.
The script is designed to work with JSON data where the keys have nested dictionaries and the values are lists of dictionaries with a "text" key.


