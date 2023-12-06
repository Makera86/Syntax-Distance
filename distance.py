# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 07:07:58 2023

@author: msi
"""

import stanza

def build_dependency_tree(sentence):
    nlp = stanza.Pipeline('en')
    doc = nlp(sentence)

    tree_map = {}
    words_list = []
    for sent in doc.sentences:
        for word in sent.words:
            tree_map[word.id - 1] = word.head - 1
            words_list.append(word.text)

    return tree_map, words_list

def calculate_edge_distance(tree_map, source_node, target_node):
    if source_node == target_node:
        return 0

    # Convert tree_map to a bi-directional graph
    graph = {}
    for child, parent in tree_map.items():
        if parent >= 0:
            graph.setdefault(child, []).append(parent)
            graph.setdefault(parent, []).append(child)

    # BFS to find shortest path
    visited = set()
    queue = [(source_node, 0)]
    while queue:
        current, distance = queue.pop(0)
        if current == target_node:
            return distance
        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                queue.append((neighbor, distance + 1))

    return float('inf')

def main():
    sentence = "The food is surprisingly good, and the decor is nice."
    aspect_word = "decor"

    tree_map, words_list = build_dependency_tree(sentence)

    aspect_word_index = None
    for index, word in enumerate(words_list):
        if word.lower().strip(".,?!") == aspect_word.lower():
            aspect_word_index = index
            break

    if aspect_word_index is not None:
        distances = {}
        for node in range(len(words_list)):
            distance = calculate_edge_distance(tree_map, aspect_word_index, node)
            distances[words_list[node]] = distance if distance != float('inf') else 'No path'

        for word, distance in distances.items():
            print(f"Distance from '{aspect_word}' to '{word}': {distance}")
    else:
        print(f"The aspect word '{aspect_word}' was not found in the sentence.")

if __name__ == "__main__":
    main()
