
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
import networkx as nx
import json
import scipy
import numpy as np
import obonet

def semantic_similarity(descendants:list, query: str):
    list_dict = []
    queries = []
    ontology = query.split(':')
    ontology_id = ontology[0]
    path = "beacon/ontologies/" + ontology_id + ".obo"
    graph = obonet.read_obo(path)
    id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
    queries.append(id_to_name[query])
    corpus = []
    for descendant in descendants:
        dict={}
        label = id_to_name[descendant]
        dict['label'] = label
        dict['id'] = descendant
        list_dict.append(dict)
        corpus.append(label)
    model = SentenceTransformer('distiluse-base-multilingual-cased', device='cpu') 
    corpus_embeddings = model.encode(corpus)
    query_embeddings = model.encode(queries)
    closest_n = 10
    for query, query_embedding in zip(queries, query_embeddings):
        distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]
        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])
        for idx, distance in results[0:closest_n]:
            for elem in list_dict:
                if corpus[idx] in elem['label']:
                    elem['distance'] = (1-distance)
    return list_dict

hola = semantic_similarity([
      'NCIT:C86031',
      'NCIT:C54014',
      'NCIT:C46113',
      'NCIT:C46108',
      'NCIT:C161316',
      'NCIT:C46110'
    ], 'NCIT:C16576')

print(hola)


