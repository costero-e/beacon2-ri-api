import networkx
import obonet

url = '/Users/oriol/Desktop/ncit.obo'
graph = obonet.read_obo(url)



# Number of nodes
len(graph)

# Number of edges
graph.number_of_edges()


networkx.is_directed_acyclic_graph(graph)

# Mapping from term ID to name
#id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
#id_to_name['NCIT:C173381']  
#for id_, data in graph.nodes(data=True):
    #print (id_)
    #print(data.get('name'))
#print(id_to_name['NCIT:C143048'] )

descendants = networkx.ancestors(graph, 'NCIT:C173381')

print(descendants)

