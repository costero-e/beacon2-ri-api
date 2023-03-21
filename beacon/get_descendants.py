import obonet
import networkx

def get_descendants_and_similarities(ontology:str): 
    ontology_list = ontology.split(':')    
    url = "ontologies/{}.obo".format(ontology_list[0])
    list_of_cousins = []
    list_of_brothers = []
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
        for list in list_of_grandpas:
            for item in list:
                successors = [n for n in graph.predecessors(item)]
                if ontology not in successors:
                    list_of_cousins.append(successors)

        for list in list_of_brothers:
            for item in list:
                similarity_high.append(item)
                similarity_medium.append(item)
                similarity_low.append(item)

        for list in list_of_cousins:
            for item in list:
                similarity_low.append(item)

        for item in similarity_medium:
            successors = [n for n in graph.predecessors(item)]
            for successor in successors:
                similarity_low.append(successor)
                similarity_medium.append(successor)
    except Exception:
        similarity_high=[]
        similarity_medium=[]
        similarity_low=[]
    
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

with open('filtering_terms.txt', 'r') as f:
    for line in f:
        line = line.replace("\n","")
        get_descendants_and_similarities(line)
        print('done')
