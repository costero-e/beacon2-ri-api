import obonet
import networkx
import json

def get_descendants_and_similarities(ontology:str):
    ontology_list = ontology.split(':')    
    url = "ontologies/{}.obo".format(ontology_list[0])
    list_of_cousins = []
    list_of_brothers = []
    list_of_uncles = []
    list_of_grandpas = []
    url_alt = "https://www.ebi.ac.uk/efo/EFO.obo"
    try:
        graph = obonet.read_obo(url)
    except Exception:
        graph = obonet.read_obo(url_alt)
    try:
        descendants = networkx.ancestors(graph, ontology)
    except Exception:
        descendants = ''
    descendants=list(descendants)
    print(descendants)
    path = "descendants/{}{}.txt".format(ontology_list[0],ontology_list[1])
    with open(path, 'w') as f:
        for item in descendants:
            f.write(item+"\n")
    f.close()
    try:
        tree = [n for n in graph.successors(ontology)]
        for onto in tree:
            predecessors = [n for n in graph.successors(onto)]
            successors = [n for n in graph.predecessors(onto)]
            list_of_brothers.append(successors)
            list_of_grandpas.append(predecessors)
        similarity_high=[]
        similarity_medium=[]
        similarity_low=[]
        for llista in list_of_grandpas:
            for item in llista:
                uncles = [n for n in graph.predecessors(item)]
                list_of_uncles.append(uncles)
                for uncle in uncles:
                    cousins = [n for n in graph.predecessors(uncle)]
                    if ontology not in cousins:
                        list_of_cousins.append(cousins)

        for llista in list_of_brothers:
            for item in llista:
                similarity_high.append(item)
                similarity_medium.append(item)
                similarity_low.append(item)

        for llista in list_of_cousins:
            for item in llista:
                similarity_medium.append(item)
                similarity_low.append(item)
        
        for llista in list_of_uncles:
            for item in llista:
                similarity_low.append(item)

    except Exception:
        similarity_high=[]
        similarity_medium=[]
        similarity_low=[]
    dict={}
    dict[ontology]={}
    dict[ontology]['descendants']=descendants
    dict[ontology]['similarity_high']=similarity_high
    dict[ontology]['similarity_medium']=similarity_medium
    dict[ontology]['similarity_low']=similarity_low
    
    path = "similarities/{}{}{}.txt".format(ontology_list[0],ontology_list[1],'high')
    with open(path, 'w') as f:
        for item in similarity_high:
            f.write(item+"\n")
    f.close()
    path = "similarities/{}{}{}.txt".format(ontology_list[0],ontology_list[1],'medium')
    with open(path, 'w') as f:
        for item in similarity_medium:
            f.write(item+"\n")
    f.close()
    path = "similarities/{}{}{}.txt".format(ontology_list[0],ontology_list[1],'low')
    with open(path, 'w') as f:
        for item in similarity_low:
            f.write(item+"\n")
    f.close()
    
i=0
with open('filtering_terms.txt', 'r') as f:
    for line in f:
        i +=1
        line = line.replace("\n","")
        get_descendants_and_similarities(line)
        print(i)
    
