from fastapi import FastAPI
from pydantic import BaseModel
from transformers import DistilBertTokenizerFast
from MultiLabelSequenceClassification import DistilBertForMultiLabelSequenceClassification
import torch
import pickle

app = FastAPI()

# Initialize the tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

# Load the model
model = DistilBertForMultiLabelSequenceClassification.from_pretrained('./model')

# Load the MultiLabelBinarizer
with open('./model/mlb.pkl', 'rb') as f:
    mlb = pickle.load(f)

class Item(BaseModel):
    question: str

@app.post("/predict/")
async def create_item(item: Item):
    # Tokenize the question
    inputs = tokenizer(item.question, truncation=True, padding=True, return_tensors="pt")

    # Make a prediction
    logits = model(**inputs).logits

    # Apply the sigmoid function to the logits
    probs = torch.sigmoid(logits)

    # Convert the probabilities to a binary format
    threshold = 0.5
    predictions = (probs > threshold).int()

    # Convert the binary predictions back to the original labels
    predicted_intents = mlb.inverse_transform(predictions.detach().numpy())

    return {"predicted_intents": predicted_intents}

