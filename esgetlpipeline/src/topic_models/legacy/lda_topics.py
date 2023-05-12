#!/usr/bin/env python

# Author: Jude Safo
# Version: 1
# Changes:
# Example: python lda_topics.py


import json
import re
from typing import List, Tuple
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download NLTK resources
import nltk

nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

# Instantiate lemmatizer and set of stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def preprocess_text(text: str) -> List[str]:
    """Preprocesses text by tokenizing, removing punctuation, stop words, and lemmatizing.

    Args:
        text (str): The input text to be preprocessed.

    Returns:
        List[str]: A list of preprocessed tokens.
    """
    # Tokenize, remove punctuation, stopwords, and lemmatize
    tokens = word_tokenize(text)
    tokens = [re.sub(r"\W", "", token).lower() for token in tokens]
    tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token not in stop_words and len(token) > 2
    ]
    return tokens


def perform_topic_modeling(
    text: str, num_topics: int = 5, num_keywords: int = 10
) -> List[Tuple[int, str]]:
    """Performs topic modeling on the input text using Latent Dirichlet Allocation (LDA).

    Args:
        text (str): The input text to be analyzed.
        num_topics (int, optional): The number of topics to extract from the text. Defaults to 5.
        num_keywords (int, optional): The number of keywords to include for each topic. Defaults to 10.

    Returns:
        List[Tuple[int, str]]: A list of tuples containing the topic ID and its corresponding keywords.
    """
    # Preprocess the text
    tokens = preprocess_text(text)

    # Prepare the corpus
    dictionary = corpora.Dictionary([tokens])
    corpus = [dictionary.doc2bow(token) for token in [tokens]]

    # Train the LDA model
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

    # Extract topics and their keywords
    topics = lda_model.print_topics(num_words=num_keywords)

    # Print and return the topics
    for idx, topic in topics:
        print(f"Topic {idx}: {topic}")
    return topics


# Read in the input text
with open(
    "../plaintext/Starbucks_Global_Social_Impact_Report.txt", "r", encoding="utf-8"
) as f:
    text = f.read()

# Perform topic modeling on the input text
topics = perform_topic_modeling(text, num_topics=5, num_keywords=10)

# Ensure that the output is in the expected format
assert isinstance(topics, list)
assert all(isinstance(topic, tuple) and len(topic) == 2 for topic in topics)
assert all(isinstance(topic[0], int) and isinstance(topic[1], str) for topic in topics)
