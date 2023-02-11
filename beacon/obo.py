import networkx
import obonet

# Read the taxrank ontology
url = '/Users/oriol/Desktop/ncit.obo'
graph = obonet.read_obo(url)

# Or read the xz-compressed taxrank ontology
# url = 'https://github.com/dhimmel/obonet/raw/main/tests/data/taxrank.obo.xz'
# graph = obonet.read_obo(url)

# Number of nodes
len(graph)

# Number of edges
graph.number_of_edges()

# Check if the ontology is a DAG
networkx.is_directed_acyclic_graph(graph)

# Mapping from term ID to name
id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
id_to_name['NCIT:C173381']  # TAXRANK:0000006 is species
for id_, data in graph.nodes(data=True):
    print (id_)
    print(data.get('name'))
print(id_to_name['NCIT:C143048'] )

# Find all superterms of species. Note that networkx.descendants gets
# superterms, while networkx.ancestors returns subterms.
descendants = networkx.descendants(graph, 'NCIT:C173381')

#print(descendants)

