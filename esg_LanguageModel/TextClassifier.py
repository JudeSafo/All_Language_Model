#!/usr/bin/env python3

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sys
import pickle

def predict_intent(sentence):
    model_path = './model'
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

    # Load the MultiLabelBinarizer
    with open(f'{model_path}/mlb.pkl', 'rb') as f:
        mlb = pickle.load(f)

    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model(**inputs)
    probs = torch.sigmoid(outputs.logits)
    threshold = 0.051
    preds = (probs > threshold).int()

    # Check if the maximum probability is below the threshold
    if torch.max(probs) < threshold:
        print("I don't have that answer")
    else:
        # Transform the predicted labels back to their original form
        labels = mlb.inverse_transform(preds.detach().numpy())
        # Convert the tuple to a list
        labels = [list(label) for label in labels]
        # Get the prediction confidence for the predicted labels
        confidences = [probs[0, mlb.classes_.tolist().index(label)].item() for label in labels[0]]
        # Combine the labels and confidences into a list of tuples
        result = list(zip(labels[0], confidences))
        print(f"Predicted labels and confidences: {result}")

if __name__ == "__main__":
    sentence = sys.argv[1]
    predict_intent(sentence)

