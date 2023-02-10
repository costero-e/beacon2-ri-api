from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
import networkx as nx
import json
import numpy


def create_model(ontology):
    sentences = []

    model = SentenceTransformer('distilbert-base-nli-mean-tokens')

    path = ontology.replace('/','')
    complete_path = 'ontologies/' + path + '.json'

    f = open(complete_path)
    data = json.load(f)
    for onto in data:
        sentences.append(onto['label'])

    print(len(sentences))

    sentence_embeddings = model.encode(sentences)

    save_path = 'sentence_embeddings/' + path + '.txt'

    numpy.savetxt(save_path, sentence_embeddings)
