#!/usr/bin/env python3

"""
This script fine-tunes a pre-trained DistilBERT model from the Hugging Face Transformers library on an intent classification task. The task involves mapping questions to a set of predefined intents.

The script performs the following steps:

1. Loads the training and validation data from CSV files.
2. Tokenizes the questions using the DistilBERT tokenizer.
3. Converts the intents into a binary format using a MultiLabelBinarizer.
4. Creates PyTorch Datasets for the training and validation data.
5. Initializes a DistilBERT model for sequence classification, with the number of labels equal to the number of unique intents.
6. Defines a set of training arguments, including the number of training epochs and the batch size.
7. Initializes a Trainer, which is a class provided by the Transformers library for training and evaluating models.

To run the script, you need to have the following installed:

- Python 3.6 or later
- PyTorch 1.0.0 or later
- Transformers 4.0.0 or later
- scikit-learn 0.20.0 or later
- pandas 0.23.0 or later

You also need to have the training and validation data in the correct format. The data should be in a CSV file, with one column for the questions and one column for the intents. The intents should be in a list format.

Example:

Question,Intents
"How does Kraft Heinz address efficiency projects?",['efficiency projects']
"How as Kraft Heinz integrated energy efficiency into procurement?",['energy efficiency', 'procurement']

You can run the script from the command line as follows:

python train.py

The script will save the trained model and the MultiLabelBinarizer in the 'results' directory.
"""

import argparse
import pandas as pd
import pickle
from sklearn.preprocessing import MultiLabelBinarizer
from MultiLabelSequenceClassification import DistilBertForMultiLabelSequenceClassification
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset
import torch
import datetime
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


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
    Loads the data from a pickle file.

    Args:
        file_path (str): The path to the pickle file.

    Returns:
        df (pd.DataFrame): The loaded data.
    """
    try:
        df = pd.read_pickle(file_path)
        print_timestamped_message(f"Data loaded successfully from {file_path}")
        return df
    except Exception as e:
        print_timestamped_message(f"Error occurred while loading data: {e}")
        raise

def main():
    train_file_path = "../data/train.pkl"
    val_file_path = "../data/val.pkl"

    # Load the training and validation data
    train_df = load_data(train_file_path)
    print_timestamped_message(f"Loaded training data with shape {train_df.shape}")
    val_df = load_data(val_file_path)
    print_timestamped_message(f"Loaded validation data with shape {val_df.shape}")

    # Initialize the tokenizer
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

    # Tokenize the questions
    train_encodings = tokenizer(train_df['Question'].tolist(), truncation=True, padding=True)
    print_timestamped_message(f"Tokenized training questions")
    val_encodings = tokenizer(val_df['Question'].tolist(), truncation=True, padding=True)
    print_timestamped_message(f"Tokenized validation questions")


    # Initialize the MultiLabelBinarizer
    mlb = MultiLabelBinarizer()

    # Transform the intents into binary format
    train_labels = mlb.fit_transform(train_df['Intents'])
    print_timestamped_message(f"Transformed training intents into binary format")
    val_labels = mlb.transform(val_df['Intents'])
    print_timestamped_message(f"Transformed validation intents into binary format")


    # Create the datasets
    train_dataset = IntentClassificationDataset(train_encodings, train_labels)
    print_timestamped_message(f"Created training dataset")
    val_dataset = IntentClassificationDataset(val_encodings, val_labels)
    print_timestamped_message(f"Created validation dataset")


    # Initialize the model
    model = DistilBertForMultiLabelSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=len(mlb.classes_))
    print_timestamped_message(f"Initialized model")


    # then in your training code, use args.learning_rate, args.num_train_epochs, etc.
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        per_device_eval_batch_size=args.per_device_eval_batch_size,
        learning_rate=args.learning_rate,
        warmup_steps=args.warmup_steps,
        weight_decay=args.weight_decay,
        logging_dir='./logs',
    )

    # Initialize the trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )
    print_timestamped_message(f"Initialized trainer")

    # Train the model
    trainer.train()
    print_timestamped_message(f"Trained model")

    # Save the model
    if not os.path.exists('./model'):
        os.makedirs('./model')
    model.save_pretrained('./model')

    # Save the tokenizer
    tokenizer.save_pretrained('./model')

    # Save the MultiLabelBinarizer
    with open('./model/mlb.pkl', 'wb') as f:
        pickle.dump(mlb, f)

    print_timestamped_message("Training completed successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning_rate', type=float, default=1e-5)
    parser.add_argument('--num_train_epochs', type=int, default=3)
    parser.add_argument('--per_device_train_batch_size', type=int, default=8)
    parser.add_argument('--per_device_eval_batch_size', type=int, default=64)
    parser.add_argument('--warmup_steps', type=int, default=500)
    parser.add_argument('--weight_decay', type=float, default=0.01)

    args = parser.parse_args()
    main()
