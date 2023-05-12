#!/usr/bin/env python3

"""
FastAPI implementation of the text summarization service.

To run this app:
1. Install FastAPI and Uvicorn: pip install fastapi uvicorn
2. Run the server: uvicorn main:app --reload
"""

import json
from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForQuestionAnswering
from llm_esg import TextProcessor, QuestionAnswerModel

app = FastAPI()

# Cache the summarization pipeline
qa_model_name = "deepset/roberta-base-squad2"
qa_tokenizer = AutoTokenizer.from_pretrained(qa_model_name)
qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model_name)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", tokenizer="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")


class SummaryInput(BaseModel):
    text: str
    json_file: Optional[str] = None  # Change this line
    mode: str = "lengthen"
    summary_length: int = 100

class QuestionInput(BaseModel):
    text: str
    json_file: Optional[str] = None  # Change this line


@app.post("/generate_summary", response_model=Dict[str, Any])
async def generate_summary(summary_input: SummaryInput) -> Dict[str, Any]:
    input_text = summary_input.text.strip()  # Remove leading and trailing whitespace
    json_file = summary_input.json_file
    mode = summary_input.mode  # Extract the mode from the input
    summary_length = summary_input.summary_length  # Extract the summary_length from the input


    if not input_text:
        raise HTTPException(status_code=400, detail="text field cannot be empty.")

    if len(input_text) > 10000:  # Set a maximum input length
        raise HTTPException(status_code=400, detail="text field is too long. Maximum length allowed is 10000 characters.")

    if json_file is None:
        json_file = "PostESG_report.json"

    try:
        with open(json_file, "r") as f:
            json_data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail=f"JSON file '{json_file}' not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while loading JSON data: {str(e)}")

    processor = TextProcessor(input_text, json_data, summarizer, mode)  # Pass the mode to TextProcessor
    result = processor.run()

    return result

@app.post("/answer_question", response_model=Dict[str, Any])
async def answer_question(question_input: QuestionInput) -> Dict[str, Any]:
    """
    Given a question and optional JSON data, this function finds an answer based on the reference text.

    :param question_input: A QuestionInput object containing the question text and optional JSON data.
    :type question_input: QuestionInput
    :return: A dictionary containing the answer to the question, relevant search terms, and reference paragraph.
    :rtype: Dict[str, Any]
    """
    input_text = question_input.text.strip()  # Remove leading and trailing whitespace
    json_file = question_input.json_file
    

    if not input_text:
        raise HTTPException(status_code=400, detail="text field cannot be empty.")

    if len(input_text) > 10000:  # Set a maximum input length
        raise HTTPException(status_code=400, detail="text field is too long. Maximum length allowed is 10000 characters.")

    if json_file is None:
        json_file = "PostESG_report.json"

    try:
        with open(json_file, "r") as f:
            json_data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail=f"JSON file '{json_file}' not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while loading JSON data: {str(e)}")

    processor = TextProcessor(input_text, json_data, summarizer)  # Remove the mode variable here
    reference_paragraph = processor.get_reference_paragraph()
    relevant_search_terms = processor.find_relevant_keys()


    if reference_paragraph:
        try:
            qa_model_instance = QuestionAnswerModel(input_text, reference_paragraph, qa_model, qa_tokenizer)
            answer = qa_model_instance.get_answer()
        except Exception as e:
            print(f"Error while getting answer: {str(e)}")
            answer = "An error occurred while trying to find an answer."
    else:
        answer = "Unable to answer question"

    return {
        "answer": answer,
        "relevant_search_terms": relevant_search_terms,
        "reference_paragraph": reference_paragraph
    }
