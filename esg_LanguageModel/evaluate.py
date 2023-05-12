#!/usr/bin/env python3
"""
This script evaluates a fine-tuned DistilBERT model on an intent classification task.
"""

from sklearn.metrics import precision_recall_fscore_support, accuracy_score
import pandas as pd
import json
import ast
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score, precision_score, recall_score
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from MultiLabelSequenceClassification import DistilBertForMultiLabelSequenceClassification
from torch.utils.data import Dataset
import torch
import datetime
import pickle

class IntentClassificationDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def print_timestamped_message(message: str) -> None:
    """
    Prints a timestamped message.

    Args:
        message (str): The message to print.
    """
    print(f"[{datetime.datetime.now()}] {message}")

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads the data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        df (pd.DataFrame): The loaded data.
    """
    try:
        df = pd.read_csv(file_path)
        print_timestamped_message(f"Data loaded successfully from {file_path}")
        return df
    except Exception as e:
        print_timestamped_message(f"Error occurred while loading data: {e}")
        raise

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the data.

    Args:
        df (pd.DataFrame): The data to preprocess.

    Returns:
        df (pd.DataFrame): The preprocessed data.
    """
    def parse_intents(intents_str):
        try:
            return ast.literal_eval(intents_str)
        except (SyntaxError, ValueError):
            print(f"Could not parse intents string: {intents_str}")
            return []

    try:
        # Convert intents from string to list
        df['Intents'] = df['Intents'].apply(parse_intents)
        print_timestamped_message("Data preprocessed successfully")
        return df
    except Exception as e:
        print_timestamped_message(f"Error occurred while preprocessing data: {e}")
        raise

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.sigmoid(torch.from_numpy(logits))
    predictions = predictions > 0.3
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='micro')

    acc = accuracy_score(labels, predictions)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def main():
    # Load the validation data
    val_file_path = "../data/val.csv"
    val_df = load_data(val_file_path)

    # Preprocess the validation data
    val_df = preprocess_data(val_df)

    # Initialize the tokenizer
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

    # Tokenize the questions
    val_encodings = tokenizer(val_df['Question'].tolist(), truncation=True, padding=True)

    # Load the MultiLabelBinarizer
    with open('./model/mlb.pkl', 'rb') as f:
        mlb = pickle.load(f)

    # Transform the intents into binary format
    val_labels = mlb.transform(val_df['Intents'])

    # Create the dataset
    val_dataset = IntentClassificationDataset(val_encodings, val_labels)

    # Initialize the model
    model = DistilBertForMultiLabelSequenceClassification.from_pretrained('./model')

    # Define the training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        per_device_eval_batch_size=64,
    )

    # Initialize the trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    # Evaluate the model
    eval_result = trainer.evaluate()

    # Print the evaluation metrics
    print(eval_result)

    # Save the evaluation metrics to a JSON file
    with open('evaluation_metrics.json', 'w') as f:
        json.dump(eval_result, f)

if __name__ == "__main__":
    main()

