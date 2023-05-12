#!/usr/bin/env python

import numpy as np
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize
from typing import List
import nltk

# Download NLTK resources
nltk.download("punkt")


def cluster_sentences(input_file: str, num_clusters: int = 5) -> List[List[str]]:
    """Clusters the sentences in an input file using K-means clustering.

    Args:
        input_file (str): The input file to be clustered.
        num_clusters (int, optional): The number of clusters to generate. Defaults to 5.

    Returns:
        List[List[str]]: A list of clusters, each containing a list of sentences.
    """
    # Load the pre-trained transformer model
    model = SentenceTransformer("distilbert-base-nli-mean-tokens")

    # Read and tokenize the input file
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    sentences = sent_tokenize(text)

    # Generate embeddings for the sentences
    embeddings = model.encode(sentences)

    # Perform clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(embeddings)

    # Assign sentences to clusters
    clusters = [[] for _ in range(num_clusters)]
    for sentence, cluster_id in zip(sentences, kmeans.labels_):
        clusters[cluster_id].append(sentence)

    # Print and return clusters
    for idx, cluster in enumerate(clusters):
        print(f"Cluster {idx}:")
        print("\n".join(cluster[:5]))  # Print the first 5 sentences in each cluster
        print("\n")

    return clusters


# Run the clustering algorithm on the input file
if __name__ == "__main__":
    input_file = "../plaintext/Starbucks_Global_Social_Impact_Report.txt"
    num_clusters = 5

    try:
        clusters = cluster_sentences(input_file, num_clusters)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    # Ensure that the output is in the expected format
    assert isinstance(clusters, list)
    assert all(isinstance(cluster, list) for cluster in clusters)
    assert all(
        isinstance(sentence, str) for cluster in clusters for sentence in cluster
    )
