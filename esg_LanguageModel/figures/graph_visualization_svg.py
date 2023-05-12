#!/usr/bin/env python3

"""
This script reads a JSON file containing a knowledge graph and generates an SVG visualization using NetworkX,
Matplotlib, and PyGraphviz.

Usage:
    python knowledge_graph_visualization.py -i INPUT_FILE -o OUTPUT_FILE
"""

#!/usr/bin/env python3

import os
import argparse
import json
import networkx as nx
from graphviz import Source


def read_json_file(file_path: str) -> dict:
    """Read JSON data from a file.

    Args:
        file_path (str): Path to the input JSON file.

    Returns:
        dict: JSON data as a dictionary.
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def draw_knowledge_graph(knowledge_graph: dict, output_file: str) -> None:
    """Draw the knowledge graph using NetworkX and Graphviz.

    Args:
        knowledge_graph (dict): Knowledge graph data as a dictionary.
        output_file (str): Path to the output SVG file.
    """
    G = nx.DiGraph()

    for node in knowledge_graph['nodes']:
        G.add_node(node)

    for edge in knowledge_graph['edges']:
        G.add_edge(edge['source'], edge['target'], label=edge['token'])

    dot_format = nx.nx_pydot.to_pydot(G).to_string()
    src = Source(dot_format, format='svg')
    src.render(output_file, cleanup=True)


def main(input_file: str, output_file: str) -> None:
    """Main function of the script.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output SVG file.
    """
    knowledge_graph = read_json_file(input_file)
    draw_knowledge_graph(knowledge_graph, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an SVG visualization of a knowledge graph")
    parser.add_argument("-i", "--input-file", type=str, required=True, help="Path to the input JSON file")
    parser.add_argument("-o", "--output-file", type=str, help="Path to the output SVG file (optional)")

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file or os.path.splitext(input_file)[0] + ".svg"

    main(input_file, output_file)
