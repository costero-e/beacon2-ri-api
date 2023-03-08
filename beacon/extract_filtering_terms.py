import os.path
import urllib.request
from typing import List, Dict, Optional
import re
from urllib.error import HTTPError

import requests
import owlready2
from pymongo.mongo_client import MongoClient
import progressbar
from bson.objectid import ObjectId
from owlready2 import OwlReadyOntologyParsingError
from tqdm import tqdm
import obonet
from bson.json_util import dumps
import json
import networkx
import os


ONTOLOGY_REGEX = re.compile(r"([_A-Za-z]+):([_A-Za-z0-9^\-]+)")

client = MongoClient(
    "mongodb://127.0.0.1:27017/"
    #"mongodb://root:example@mongo:27017/beacon?authSource=admin"

)

class MyProgressBar:
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num: int, block_size: int, total_size: int):
        if not self.pbar:
            self.pbar = progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()

def insert_all_ontology_terms_used():
    collections = client.beacon.list_collection_names()
    if 'filtering_terms' in collections:
        collections.remove('filtering_terms')
    print("Collections:", collections)
    for c_name in collections:
        terms_ids = find_ontology_terms_used(c_name)
        terms = get_filtering_object(terms_ids, c_name)
        if len(terms) > 0:
            client.beacon.filtering_terms.insert_many(terms)


def get_ontology_name(ontology: owlready2.Ontology) -> str:
    path = "ontologies/{}.obo".format(ontology)
    try:
        graph = obonet.read_obo(path)
        name = graph.graph['remark']
        if '.' in name[0]:
            list_name = name[0].split('.')
            name = list_name[0]
        return name
    except:
        pass

def load_ontology(ontology_id: str) -> Optional[owlready2.Ontology]:
    if ontology_id.isalpha():
        url_alt = "https://www.ebi.ac.uk/efo/EFO.obo"
        url = "http://purl.obolibrary.org/obo/{}.obo".format(ontology_id.lower())
        path = "ontologies/{}.obo".format(ontology_id)
        try:
            if not os.path.exists(path):
                urllib.request.urlretrieve(url, path, MyProgressBar())
        except HTTPError:
            # TODO: Handle error
            print("ERROR", HTTPError)
            pass
        except ValueError:
            print("ERROR", ValueError)
            pass
        try:
            print (os.stat(path).st_size)
            if os.stat(path).st_size == 0:
                try:
                    urllib.request.urlretrieve(url_alt, path, MyProgressBar())
                except HTTPError:
                    # TODO: Handle error
                    print("ERROR", HTTPError)
                    pass
                except ValueError:
                    print("ERROR", ValueError)
                    pass
        except Exception:
                pass
    return '{}'.format(ontology_id)

def get_ontology_term_count(collection_name: str, term: str) -> int:
    query = {
        '$text': {
            '$search': '\"' + term + '\"'
        }
    }
    return client.beacon\
        .get_collection(collection_name)\
        .count_documents(query)

'''

def get_ontology_field_name(ontology_id:str, term_id:str, collection:str):
    query = {
        '$text': {
            '$search': '\"' + ontology_id + ":" + term_id + '\"'
        }
    }
    results = client.beacon.get_collection(collection).find(query)
    results = list(results)
    results = dumps(results)
    results = json.loads(results)
    field = ''
    for result in results:
        for k, v in result.items():
            if isinstance(v, str): 
                if v == ontology_id + ':' + term_id:
                    field = k
                    break
            elif isinstance(v, dict):
                for k2, v2 in v.items():
                    if v2 == ontology_id + ':' + term_id:
                        field = k + '.' + k2
                        break 
            elif isinstance(v, list):
                for item in v:
                    #print(item)
                    if isinstance(item, str): 
                        if item == ontology_id + ':' + term_id:
                            field = item
                            break
                    elif isinstance(item, dict):
                        for k2, v2 in item.items():
                            if isinstance(v2, str):
                                if v2 == ontology_id + ':' + term_id:
                                    field = k2
                                    break 
                            elif isinstance(v2, dict):
                                for k3, v3 in v2.items():
                                    if isinstance(v3, str):
                                        if v3 == ontology_id + ':' + term_id:
                                            field = k2 + '.' + k3
                                            break 
                                    elif isinstance(v3, dict):
                                        for k4, v4 in v3.items():
                                            if v4 == ontology_id + ':' + term_id:
                                                field = k2 + '.' + k3 + '.' + k4
                                                break

        #print(field)

    return field'''

def get_descendants(ontology_id:str, ontology_term:str):
    if ontology_id == 'GAZ':
        descendants = ''
    else:        
        url = 'ontologies/{}.obo'.format(ontology_id.upper())
        url_alt = "https://www.ebi.ac.uk/efo/EFO.obo"
        label=''
        try:
            graph = obonet.read_obo(url)
            networkx.is_directed_acyclic_graph(graph)
        except Exception:
            graph = obonet.read_obo(url_alt)
            networkx.is_directed_acyclic_graph(graph)
        try:
            id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
            label = id_to_name['{}:{}'.format(ontology_id,ontology_term)]
        except Exception:
            pass
    ontology = ontology_id + ':' + ontology_term
    

    try:
        descendants = networkx.descendants(graph, ontology)
    except Exception:
        descendants = ''
    if not descendants:
        descendants = {ontology}
    descendants = list(descendants)
    dict = {}

    try:
        dict['label']=label
    except Exception:
        dict['label']=''
    
    dict['descendants']=descendants
    try:
        dict['list']=id_to_name
    except Exception:
        list_onto=[]
        list_onto.append(ontology)
        dict['list']=list_onto


    dict['ontology']='{}'.format(ontology_id)
    #print(descendants)
    return dict

def get_descendants_with_list(ontology_id:str, ontology_term:str):        
    url = 'ontologies/{}.obo'.format(ontology_id.upper())
    url_alt = "https://www.ebi.ac.uk/efo/EFO.obo"
    try:
        graph = obonet.read_obo(url)
    except Exception:
        graph = obonet.read_obo(url_alt)
    ontology = ontology_id + ':' + ontology_term
    networkx.is_directed_acyclic_graph(graph)
    try:
        descendants = networkx.descendants(graph, ontology)
    except Exception:
        descendants = ''
    if not descendants:
        descendants = {ontology}
    descendants = list(descendants)
    dict = {}
    dict['descendants']=descendants
    dict['ontology']='{}'.format(ontology_id)
    #print(descendants)
    return dict

def find_ontology_terms_used(collection_name: str) -> List[Dict]:
    terms_ids = []
    count = client.beacon.get_collection(collection_name).estimated_document_count()
    xs = client.beacon.get_collection(collection_name).find()
    for r in tqdm(xs, total=count):
        matches = ONTOLOGY_REGEX.findall(str(r))
        for ontology_id, term_id in matches:
            term = ':'.join([ontology_id, term_id])
            print(term, ontology_id)
            if term not in terms_ids:
                terms_ids.append(term)
    print(terms_ids)
    return terms_ids

def get_filtering_object(terms_ids: list, collection_name: str):
    terms = []
    ontologies = dict()
    array = []
    for onto in terms_ids:
        ontology = onto.split(':')
        ontology_id = ontology[0]
        term_id = ontology[1]
        if ontology_id not in ontologies:
            ontologies[ontology_id] = load_ontology(ontology_id)
        if ontology_id not in array:
            if ontologies[ontology_id] is not None:
                dict_descendants = get_descendants(ontology_id, term_id)
                array = dict_descendants['ontology']
                ontologies['list'] = dict_descendants['list']
        if ontology_id in array:
            dict_descendants = get_descendants_with_list(ontology_id, term_id)
            id_to_name = ontologies['list']
            try:
                dict_descendants['label']= id_to_name['{}:{}'.format(ontology_id,term_id)]
            except Exception:
                dict_descendants['label']=''
        if dict_descendants['label'] != '':
                terms.append({
                        'type': get_ontology_name(ontologies[ontology_id]),
                        'id': onto,
                        'label': dict_descendants['label'],
                        # TODO: Use conf.py -> beaconGranularity to not disclouse counts in the filtering terms
                        'count': get_ontology_term_count(collection_name, onto),
                        'collection': collection_name,

                        #'field': get_ontology_field_name(ontology_id, term_id, collection_name),

                        'descendants': dict_descendants['descendants'],
                        #'similarity':
                    })
        print(terms)
    return terms


def get_alphanumeric_term_count(collection_name: str, key: str) -> int:
    return len(client.beacon\
        .get_collection(collection_name)\
        .distinct(key))


def get_properties_of_document(document, prefix="") -> List[str]:
    properties = []
    if document is None or isinstance(document, str) or isinstance(document, int):
        return []
    elif isinstance(document, list):
        for elem in document:
            properties += get_properties_of_document(elem, prefix)
    elif isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                continue
            elif value is None:
                properties.append(prefix + '.' + key if prefix else key)
            elif isinstance(value, int):
                properties.append(prefix + '.' + key if prefix else key)
            elif isinstance(value, str):
                properties.append(prefix + '.' + key if prefix else key)
            elif isinstance(value, list):
                properties += get_properties_of_document(value, prefix + '.' + key if prefix else key)
            elif isinstance(value, dict):
                properties += get_properties_of_document(value, prefix + '.' + key if prefix else key)
            else:
                print('Unknown type:', value, ' (', type(value), ')')
                exit(0)
    else:
        print('Unknown type2:', document, ' (', type(document), ')')
        exit(0)
    return properties


def find_alphanumeric_terms_used(collection_name: str) -> List[Dict]:
    terms = []
    terms_ids = set()
    count = client.beacon.get_collection(collection_name).estimated_document_count()
    xs = client.beacon.get_collection(collection_name).find()
    for r in tqdm(xs, total=count):
        properties = get_properties_of_document(r)
        for p in properties:
            if p not in terms_ids:
                terms_ids.add(p)
                terms.append({
                    'type': 'alphanumeric',
                    'id': p,
                    'count': get_alphanumeric_term_count(collection_name, p),
                    'collection': collection_name,
                })
    return terms


def insert_all_alphanumeric_terms_used():
    collections = client.beacon.list_collection_names()
    if 'filtering_terms' in collections:
        collections.remove('filtering_terms')
    collections = ['runs']
    print("Collections:", collections)
    for c_name in collections:
        terms = find_alphanumeric_terms_used(c_name)
        #print(terms)
        if len(terms) > 0:
            client.beacon.filtering_terms.insert_many(terms)


insert_all_ontology_terms_used()
#insert_all_alphanumeric_terms_used()
#terms=find_ontology_terms_used("individuals")
#print(terms)
#hola = get_ontology_term_label('NCIT','C173381')
#print(hola)
#hola = find_alphanumeric_terms_used('analyses')
#print(hola)
