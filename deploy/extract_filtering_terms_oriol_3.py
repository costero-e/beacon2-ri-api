from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
import networkx as nx
import json
import numpy

sentences = []

model = SentenceTransformer('distilbert-base-nli-mean-tokens')

f = open('ontologies/ontologies.json')
data = json.load(f)
for ontology in data:
    sentences.append(ontology['label'])

print(len(sentences))

loop = len(sentences)

sentence_embeddings = model.encode(sentences)

numpy.savetxt('sentence_embeddings.txt', sentence_embeddings)
