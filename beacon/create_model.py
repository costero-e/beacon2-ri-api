from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
import networkx as nx
import json
import numpy


def create_model():
    sentences = ['XY Female', 'Castrated Female', 'Female Phenotype', 'Female', 'Self-Report', 'Female of Childbearing Potential', 'Female Gender']

    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    '''
    path = ontology.replace('/','')
    complete_path = 'ontologies/' + path + '.json'

    f = open(complete_path)
    data = json.load(f)
    for onto in data:
        sentences.append(onto['label'])

    print(len(sentences))
    '''
    sentence_embeddings = model.encode(sentences)

    save_path = 'sentence_embeddings/' + 'prova' + '.txt'

    numpy.savetxt(save_path, sentence_embeddings)

create_model()