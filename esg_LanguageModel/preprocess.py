#!/usr/bin/env python3
"""
This script loads and preprocesses the data for intent classification.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple
import ast
import datetime

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
        df = pd.read_csv(file_path, on_bad_lines='skip')
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
    try:
        # Convert intents from string to list
        df['Intents'] = df['Intents'].apply(lambda x: ast.literal_eval(x) if (x and x.startswith('[') and x.endswith(']')) else [])
        print_timestamped_message("Data preprocessed successfully")
        return df
    except Exception as e:
        print_timestamped_message(f"Error occurred while preprocessing data: {e}")
        raise

def split_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the data into a training set and a validation set.

    Args:
        df (pd.DataFrame): The data to split.
        test_size (float): The proportion of the data to include in the test split.
        random_state (int): The seed used by the random number generator.

    Returns:
        train_df (pd.DataFrame): The training data.
        val_df (pd.DataFrame): The validation data.
    """
    try:
        train_df, val_df = train_test_split(df, test_size=test_size, random_state=random_state)
        print_timestamped_message("Data split into training and validation sets")
        return train_df, val_df
    except Exception as e:
        print_timestamped_message(f"Error occurred while splitting data: {e}")
        raise

def main():
    file_path = "../data/data.csv"  
    df = load_data(file_path)
    df = preprocess_data(df)
    train_df, val_df = split_data(df)

    # Save the DataFrames in pickle format
    train_df.to_pickle("../data/train.pkl")
    val_df.to_pickle("../data/val.pkl")

if __name__ == "__main__":
    main()

