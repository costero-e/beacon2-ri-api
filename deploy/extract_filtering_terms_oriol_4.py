from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
import networkx as nx
import json
import numpy
''''
f = open('ontologies/ontologies.json')
data = json.load(f)

sentences = []

sentences.append(data[0])
sentences.append(data[1])
'''
sentences=['mandibular ramus','neural crest-derived structure']

model = SentenceTransformer('distilbert-base-nli-mean-tokens')

sentence_embeddings = model.encode(sentences)

length = (1 - distance.cosine(sentence_embeddings[0], sentence_embeddings[1]))

print(length)
