#!/usr/bin/env python3

# Extracts the most relevant n-grams for a set of predefined topics from a given text.

# Requires the following libraries:
#    - spacy
#    - nltk

# The script reads a plaintext file, preprocesses it, and calculates n-grams. It then extracts the top n-grams
# for each predefined topic based on their PMI score.

# Example usage:
#    python nltk_topics -i <file_path>

# Author: Jude Safo
# Date: 04/09/2023

import os
import spacy
import re
import argparse
import json
from typing import Dict, List, Tuple

# import nltk
from nltk import FreqDist, BigramCollocationFinder, TrigramCollocationFinder
from nltk.collocations import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from utils import TextAggregator, TokenTfidfExtractor

# Predefined topics
topics = [
    "Resource Use and Circularity",
    "Product Packaging",
    "Product Design",
    "Supplier ESG Management",
    "Product Health and Safety",
    "Marketing and Labeling",
    "Biodiversity and Land Use",
    "Climate Change Impacts",
    "GHG Emissions",
    "Air Quality",
    "Waste",
    "Water and Wastewater",
    "Diversity, Equity and Inclusion",
    "Human and Labor Rights",
    "Talent Management and Training",
    "Employee Health and Safety",
    "Data Security and Privacy",
    "Food Waste and Security",
    "Community Engagement",
    "Governing Body",
    "ESG Oversight",
    "Ethics and Compliance",
    "Economic Contribution",
    "Tax Transparency",
    "Value of Sustainable Innovation",
]


class TopicNgramExtractor(TokenTfidfExtractor):
    """
    A class for extracting n-grams from a list of tokens
    """

    def __init__(
        self,
        input_path: str,
        topics: List[str],
        n: int = 15,
        nlp_model: str = "en_core_web_sm",
    ):
        super().__init__(input_path, n, topics)
        self.topics = [topic.lower() for topic in topics]  # topics
        self.text = text
        self.nlp = spacy.load(nlp_model)

        # Load stopwords from cache or download and cache them
        cache_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "stopwords.txt"
        )
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                self.stop_words = set(f.read().split())
        else:
            nltk.download("stopwords")
            self.stop_words = set(stopwords.words("english"))
            with open(cache_path, "w") as f:
                f.write(" ".join(self.stop_words))
        # Clean topics
        self._preprocess_topics()

        # Clean tokens
        self._preprocess_text()

    def extract_topic_ngrams(self) -> Dict[str, List[Tuple[str, float]]]:
        """
        Extracts the most relevant n-grams for each of the predefined topics from the given text.

        Returns:
        - topic_ngrams (Dict[str, List[Tuple[str, float]]]): A dictionary containing the most relevant n-grams for each topic.

        """
        self._preprocess_topics()
        tokens = self.preprocess_text()
        top_n_bigrams, top_n_trigrams = self.get_ngrams(tokens)

        topic_ngrams = {}
        ngram_scores = []
        for topic in self.topics:
            topic_keywords = re.findall(r"\w+", topic.lower())
            bigram_scores = [
                (bigram, BigramCollocationFinder.from_words(tokens).ngram_fd[bigram])
                for bigram in top_n_bigrams
                if any(keyword in bigram for keyword in topic_keywords)
            ]
            trigram_scores = [
                (trigram, TrigramCollocationFinder.from_words(tokens).ngram_fd[trigram])
                for trigram in top_n_trigrams
                if any(keyword in trigram for keyword in topic_keywords)
            ]
            ngram_scores.extend(bigram_scores + trigram_scores)
            topic_ngrams[self.final_topics[topic]] = ngram_scores

        return topic_ngrams

    def get_ngrams(self, tokens: List[str]) -> Tuple[List[str], List[str]]:
        """
        Extracts the top 50 bigrams and trigrams from a list of tokens using Pointwise Mutual Information (PMI) score.

        Args:
            tokens: A list of tokens.

        Returns:
            A tuple containing the top 50 bigrams and trigrams.
        """
        bigram_measures = BigramAssocMeasures()
        trigram_measures = TrigramAssocMeasures()
        bigram_finder = BigramCollocationFinder.from_words(tokens)
        trigram_finder = TrigramCollocationFinder.from_words(tokens)

        bigram_finder.apply_freq_filter(1)
        trigram_finder.apply_freq_filter(1)

        top_n_bigrams = bigram_finder.nbest(bigram_measures.pmi, 50)
        top_n_trigrams = trigram_finder.nbest(trigram_measures.pmi, 50)

        # Assert statements to validate the output
        assert isinstance(top_n_bigrams, list), "top_n_bigrams should be a list"
        assert isinstance(top_n_trigrams, list), "top_n_trigrams should be a list"

        return top_n_bigrams, top_n_trigrams

    def _preprocess_topics(self) -> None:
        """
        Preprocesses a given topic by removing conjunctions and relaxing the case.

        Args:
        - topic (str): The input topic to preprocess.

        Returns:
        - preprocessed_topic (str): The preprocessed topic.

        """
        processed_topics = {}
        if self.topics is None:
            return
        for topic in self.topics:
            # Remove conjunctions
            topic = topic.lower()
            topic = re.sub(r"\b(and|&)\b", "|", topic, flags=re.IGNORECASE)
            # Replace spaces in the bigrams with underscores
            topic = re.sub(r"(\w+)\s(\w+)", r"\1_\2", topic)
            # Relax case and convert words to disjunctive regular expression
            processed_topic = "|".join([t for t in re.split(r"\s+|-", topic)])
            # Replace underscores with spaces to restore bigrams
            processed_topic = processed_topic.replace("_", " ")
            processed_topics[processed_topic] = topic
        # Remove unnecessary additional |||
        processed_topics = {
            k.replace("|||", "|"): v for k, v in processed_topics.items()
        }
        # Map between the original topics and processed topics
        self.final_topics = {k: v for k, v in zip(processed_topics, self.topics)}
        # Update initial topics
        self.topics = list(processed_topics.keys())

    def preprocess_text(self) -> List[str]:
        """
        Preprocesses a given text by tokenizing, removing punctuation, stop words and lemmatizing.

        Args:
        - text (str): The input text to preprocess.

        Returns:
        - tokens (List[str]): The preprocessed tokens.

        """
        text = self.text
        max_length = 1000000  # Set the maximum chunk length
        chunks = [
            text[i : i + max_length] for i in range(0, len(text), max_length)
        ]  # Split the text into chunks

        tokens = []
        for chunk in chunks:
            doc = self.nlp(chunk)

            # Remove extraneous characters
            chunk = re.sub(r"\d+", "", chunk)  # Remove digits
            chunk = re.sub(r"\s+", " ", chunk)  # Remove extra whitespaces
            chunk = re.sub(r"\n", " ", chunk)  # Remove newlines

            tokens += [
                token.lemma_.lower()
                if not token.is_punct
                and not token.is_stop
                and token.lemma_.lower() != "-PRON-"
                else token.text.lower()
                for token in doc
                if token.is_alpha
                and (not self.stop_words or token.text.lower() not in self.stop_words)
            ]

        return tokens


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract n-grams containing specified topics from a text file or a collection of text files in a given directory"
    )
    parser.add_argument(
        "-i",
        "--input_path",
        type=str,
        help="the path to the input file or the directory containing the text files",
    )
    parser.add_argument(
        "-t",
        "--topics",
        nargs="+",
        type=str,
        help="the topics to search for in the n-grams",
    )
    args = parser.parse_args()

    # Load the text from the input file or directory
    text_aggregator = TextAggregator(args.input_path)
    text = text_aggregator.aggregate()

    # Extract the topic n-grams
    extractor = TopicNgramExtractor(text, topics)
    topic_ngrams = extractor.extract_topic_ngrams()

    # Print and save the results
    print(json.dumps(topic_ngrams, indent=2))

    with open("topic_ngrams_output.json", "w", encoding="utf-8") as f:
        json.dump(topic_ngrams, f, ensure_ascii=False, indent=2)
