import networkx
import obonet

url = '/Users/oriol/Desktop/beacon_canada/deploy/ontologies/EFO.obo'
graph = obonet.read_obo(url)

# Number of nodes
len(graph)

print(len(graph))

#print(graph.graph)
'''
data_version = graph.graph['data-version']
if '/' in data_version:
    list_data_version = data_version.split('/')
    data_version = list_data_version[1]
print(data_version)

name = graph.graph['remark']
if '.' in name[0]:
    list_name = name[0].split('.')
    name = list_name[0]
print(name)
'''
# Number of edges
graph.number_of_edges()

networkx.is_directed_acyclic_graph(graph)

# Mapping from term ID to name

#id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
#print(id_to_name['NCIT:C173381'])
#for id_, data in graph.nodes(data=True):
    #print (id_)
    #print(data.get('name'))
#print(id_to_name['NCIT:C143048'] )

descendants = networkx.ancestors(graph, 'EFO:0004600')

if not descendants:
    descendants = {''}

print(descendants)
