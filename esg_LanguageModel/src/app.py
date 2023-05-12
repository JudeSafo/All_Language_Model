#!/usr/bin/env python3

"""
FastAPI implementation of the text summarization service.

To run this app:
1. Install FastAPI and Uvicorn: pip install fastapi uvicorn
2. Run the server: uvicorn main:app --reload
"""

import json
from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from llm_esg import TextProcessor

app = FastAPI()


class SummaryInput(BaseModel):
    text: str
    json_data: Dict[str, Any] = None


@app.post("/generate_summary", response_model=Dict[str, Any])
async def generate_summary(summary_input: SummaryInput) -> Dict[str, Any]:
    """
    Generate a text summary based on the text and json_data fields.

    Args:
        summary_input (SummaryInput): An instance of SummaryInput, containing text and an optional json_data.

    Returns:
        Dict[str, Any]: The generated summary as a dictionary.

    Raises:
        HTTPException: If text is missing.
    """
    input_text = summary_input.text
    json_data = summary_input.json_data

    if input_text is None:
        raise HTTPException(status_code=400, detail="text field is required.")

    if json_data is None:
        json_file = "PostESG_report.json"
        with open(json_file, "r") as f:
            json_data = json.load(f)

    processor = TextProcessor(input_text, json_data)
    result = processor.run()

    return result

