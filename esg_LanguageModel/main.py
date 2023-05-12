#!/usr/bin/env python3

from preprocess import load_data
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.preprocessing import MultiLabelBinarizer
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

def main():
    train_file_path = "../data/train.csv"
    val_file_path = "../data/val.csv"

    # Load the training and validation data
    train_df = load_data(train_file_path)
    val_df = load_data(val_file_path)

    # Initialize the tokenizer
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

    # Tokenize the questions
    train_encodings = tokenizer(train_df['Question'].tolist(), truncation=True, padding=True)
    val_encodings = tokenizer(val_df['Question'].tolist(), truncation=True, padding=True)

    # Initialize the MultiLabelBinarizer
    mlb = MultiLabelBinarizer()

    # Transform the intents into binary format
    train_labels = mlb.fit_transform(train_df['Intents'])
    val_labels = mlb.transform(val_df['Intents'])

    # Create the datasets
    train_dataset = IntentClassificationDataset(train_encodings, train_labels)
    val_dataset = IntentClassificationDataset(val_encodings, val_labels)

    # Initialize the model
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=len(mlb.classes_))

    # Define the training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
    )

    # Initialize the trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )

    # Train the model
    trainer.train()

    # Save the model
    model.save_pretrained('./model')

    # Save the Multi

