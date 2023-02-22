import obonet
import networkx
import owlready2
from typing import List, Dict, Optional


def get_ontology_term_label(ontology: str, term: str) -> Optional[str]:
    path = "ontologies/{}.obo".format(ontology)
    try:
        graph = obonet.read_obo(path)
        id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
        return id_to_name['{}:{}'.format(ontology,term)]
    except:
        pass


'''
def get_descendants(ontology_id:str, ontology_term:str):        
    url = 'ontologies/{}.obo'.format(ontology_id)
    url_alt = 'ontologies/EFO.obo'
    try:
        graph = obonet.read_obo(url)
    except Exception:
        pass
    ontology = ontology_id + ':' + ontology_term
    #networkx.is_directed_acyclic_graph(graph)
    try:
        descendants = networkx.ancestors(graph, ontology)
    except Exception:
        descendants = ''

    if not descendants:
        descendants = {ontology}
    descendants = list(descendants)
    #print(descendants)
    return descendants
'''

hola = get_ontology_term_label('GAZ', '00150372')
#adeu = get_descendants('GAZ', '00150372')

print(hola)
#print(adeu)