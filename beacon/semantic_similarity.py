from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
import networkx as nx
import json
import numpy


def semantic_similarity(term:str, x:float):
    term_list = term.split(':')
    ontology = term_list[0].lower()

    if ontology == 'uberon':
        ontology = 'hp'
    elif ontology == 'maxo':
        ontology = 'hp'
    elif ontology == 'cl':
        ontology = 'hp'
    elif ontology == 'go':
        ontology = 'hp'

    path = ontology.replace('/','')
    complete_path = 'beacon/ontologies/' + path + '.json'
    save_path = 'beacon/sentence_embeddings/' + path + '.txt'

    f = open(complete_path)
    data = json.load(f)
    sentence_embeddings = numpy.loadtxt(save_path)


    i = 0
    for id in data:
        if term in id['id']:
            y = i
            break
        else:
            i +=1
    #print(m)

    if y != 1:
        term_to_change = data[y]
        term_1 = data[1]
        data[1] = term_to_change
        data[y] = term_1
        #print(data[m])
        #print(data[1])




    
    if y != 1:
        sentence_embeddings_to_change = sentence_embeddings[y]
        sentence_embeddings_1 = sentence_embeddings[1] 
        sentence_embeddings[1] = sentence_embeddings_to_change
        sentence_embeddings[y] = sentence_embeddings_1
        #print(sentence_embeddings[1])
        #print(sentence_embeddings[m])

    m = 1
    #print(sentence_embeddings[0])
    #print(sentence_embeddings[1])
    #print(sentence_embeddings[2])


    g = nx.DiGraph()

    list = []
    i=0
    while i < len(sentence_embeddings):
        length = (1 - distance.cosine(sentence_embeddings[i], sentence_embeddings[m]))
        list.append(length)
        i += 1
        #print(i)

    #print(list)
    #print(list[1])



    edges = []
    tuple_list = []

    n = 0

    while n < len(sentence_embeddings):
        if n != m:
            tuple_list.append(m)
            tuple_list.append(n)
            tuple_list.append({'length': list[n]})
        n+=1
        #print(n)
        edges.append(tuple(tuple_list))
        tuple_list = []

    n = 0
    edges_2=[]

    neighbours =[]

    while n < len(sentence_embeddings):
        if n == m:
            n +=1
        elif n+1 == m:
            edges_2.append(edges[n])
            edges_2.append(edges[n+2])
            edges_2.append(edges[n+3])
            g.add_edges_from(edges_2)
            lengths = nx.single_source_dijkstra_path_length(g, source=1, weight='length', cutoff=x)
            dict(lengths).keys()
            for k in dict(lengths).keys():
                if k != 1:
                    neighbours.append(k)
            edges_2 = []
            n += 4
            g = nx.DiGraph()
        elif n+1 >= len(sentence_embeddings):
            edges_2.append(edges[n])
            edges_2.append(edges[n-1])
            g.add_edges_from(edges_2)
            lengths = nx.single_source_dijkstra_path_length(g, source=1, weight='length', cutoff=x)
            for k in dict(lengths).keys():
                if k != 1:
                    neighbours.append(k)
            edges_2 = []
            n += 3
            g = nx.DiGraph()
        elif n+2 >= len(sentence_embeddings):
            edges_2.append(edges[n])
            edges_2.append(edges[n+1])
            g.add_edges_from(edges_2)
            lengths = nx.single_source_dijkstra_path_length(g, source=1, weight='length', cutoff=x)
            for k in dict(lengths).keys():
                if k != 1:
                    neighbours.append(k)
            edges_2 = []
            n += 3
            g = nx.DiGraph()
        elif n+2 == m:
            edges_2.append(edges[n])
            edges_2.append(edges[n+1])
            edges_2.append(edges[n+3])
            g.add_edges_from(edges_2)
            lengths = nx.single_source_dijkstra_path_length(g, source=1, weight='length', cutoff=x)
            for k in dict(lengths).keys():
                if k != 1:
                    neighbours.append(k)
            edges_2 = []
            n += 4
            g = nx.DiGraph()
        else:
            edges_2.append(edges[n])
            edges_2.append(edges[n+1])
            edges_2.append(edges[n+2])
            g.add_edges_from(edges_2)
            lengths = nx.single_source_dijkstra_path_length(g, source=1, weight='length', cutoff=x)
            for k in dict(lengths).keys():
                if k != 1:
                    neighbours.append(k)
            edges_2 = []
            n += 3
            g = nx.DiGraph()

    neighbours = [*set(neighbours)]

    


    n = 0
    final_neighbours = []

    while n < len(sentence_embeddings):
        if n in neighbours:
            n+=1
        else:
            final_neighbours.append(n)
            n+=1
    

    neighbours_list = []

    for a in final_neighbours:
        print(data[a])
        neighbours_list.append(data[a]['id'])
    
    if x != 1:
        del neighbours_list[1]
    #print(neighbours_list)
    return neighbours_list


list_neighbours = semantic_similarity('UBERON:0005913', 0.9)
print(list_neighbours)





