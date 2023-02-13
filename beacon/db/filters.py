from collections import defaultdict
from typing import List, Union
import re
import dataclasses
from copy import deepcopy

from beacon.request import ontologies
from beacon.request.model import AlphanumericFilter, CustomFilter, OntologyFilter, Operator, Similarity
from beacon.semantic_similarity import semantic_similarity

import logging

LOG = logging.getLogger(__name__)

CURIE_REGEX = r'^([a-zA-Z0-9]*):\/?[a-zA-Z0-9]*$'

BIOSAMPLES_FILTERS_MAP = [
    {"biosampleStatus.label" : {"$regex": ""}},
    {"characteristics.organism.text" : {"$regex": ""}},
    {"sampleOriginType.label" : {"$regex": ""}}
]

DATASETS_FILTERS_MAP = [
    {"collections.dataUseConditions.duoDataUse.label" : {"$regex": ""}},
    {"description" : {"$regex": ""}}
]

GENOMIC_VARIATIONS_FILTERS_MAP = [
    {"molecularAttributes.molecularEffects.label" : {"$regex": ""}}
]

INDIVIDUALS_FILTERS_MAP = [
    {"ethnicity.label" : {"$regex": ""}},
    {"measurementValue.quantity.unit.label":{"$regex": ""}},
    {"geographicOrigin.label":{"$regex": ""}},
    {"measures.assayCode.label":{"$regex": ""}},
    {"diseases.diseaseCode.label":{"$regex": ""}}
]

RUNS_FILTERS_MAP = [
    {"platformModel.label" : {"$regex": ""}},
    {"librarySource.label":{"$regex": ""}}
]

def apply_filters(query: dict, filters: List[dict], collection: str) -> dict:
    LOG.debug("Filters len = {}".format(len(filters)))
    if len(filters) > 0:
        query["$and"] = []
    for filter in filters:
        partial_query = {}
        if "value" in filter:
            LOG.debug(filter)
            filter = AlphanumericFilter(**filter)
            LOG.debug("Alphanumeric filter: %s %s %s", filter.id, filter.operator, filter.value)
            partial_query = apply_alphanumeric_filter(partial_query, filter)
        elif "similarity" in filter or "includeDescendantTerms" in filter or re.match(CURIE_REGEX, filter["id"]):
            filter = OntologyFilter(**filter)
            LOG.debug("Ontology filter: %s", filter.id)
            partial_query = {"$text": defaultdict(str) }
            #partial_query =  { "$text": { "$search": "" } } 
            LOG.debug(partial_query)
            partial_query = apply_ontology_filter(partial_query, filter)
        elif "text" in filter:
            LOG.debug(filter)
            filter = CustomFilter(**filter)
            LOG.debug("Text filter: %s ", filter.id)
            partial_query = apply_text_filter(filter, collection)
        else:
            filter = CustomFilter(**filter)
            LOG.debug("Custom filter: %s", filter.id)
            partial_query = apply_custom_filter(partial_query, filter)
        query["$and"].append(partial_query)
    return query


def apply_ontology_filter(query: dict, filter: OntologyFilter) -> dict:
    
    is_filter_id_required = True

    # Search similar
    if filter.similarity != Similarity.EXACT:
        is_filter_id_required = False
        if filter.similarity == Similarity.HIGH:
            cutoff = 0.9
        elif filter.similarity == Similarity.MEDIUM:
            cutoff = 0.7
        elif filter.similarity == Similarity.LOW:
            cutoff = 0.5
        similar_terms = semantic_similarity(filter.id, cutoff)
        LOG.debug("Similar: {}".format(similar_terms))
        for term in similar_terms:
            if query["$text"]["$search"]:
                query["$text"]["$search"] += " "
            query["$text"]["$search"] += term

    # Apply descendant terms
    if filter.include_descendant_terms:
        is_filter_id_required = False
        descendants = ontologies.get_descendants(filter.id)
        LOG.debug("Descendants: {}".format(descendants))
        for descendant in descendants:
            if query["$text"]["$search"]:
                query["$text"]["$search"] += " "
            query["$text"]["$search"] += descendant
    
    if is_filter_id_required:
        if query["$text"]["$search"]:
            query["$text"]["$search"] += " "
        query["$text"]["$search"] += '\"' + filter.id + '\"'

    LOG.debug("QUERY: %s", query)
    return query

def format_value(value: Union[str, List[int]]) -> Union[List[int], str, int, float]:
    if isinstance(value, list):
        return value
    elif value.isnumeric():
        if float(value).is_integer():
            return int(value)
        else:
            return float(value)
    else:
        return value

def format_operator(operator: Operator) -> str:
    if operator == Operator.EQUAL:
        return "$eq"
    elif operator == Operator.NOT:
        return "$ne"
    elif operator == Operator.GREATER:
        return "$gt"
    elif operator == Operator.GREATER_EQUAL:
        return "$gte"
    elif operator == Operator.LESS:
        return "$lt"
    else:
        # operator == Operator.LESS_EQUAL
        return "$lte"

def apply_alphanumeric_filter(query: dict, filter: AlphanumericFilter) -> dict:
    LOG.debug(filter.value)
    formatted_value = format_value(filter.value)
    formatted_operator = format_operator(filter.operator)
    if isinstance(formatted_value,list):
        query[filter.id] = { formatted_operator: formatted_value }
    #elif formatted_value.is_integer:
        #query[filter.id] = { formatted_operator: formatted_value }
    else:
        query[filter.id] = { formatted_operator: float(formatted_value) }
    query['assayCode.label']='Weight'
    LOG.debug(query)
    dict_elemmatch={}
    dict_elemmatch['$elemMatch']=query
    dict_measures={}
    dict_measures['measures']=dict_elemmatch


    LOG.debug("QUERY: %s", dict_measures)
    return dict_measures

def apply_text_filter(filter: CustomFilter, collection: str) -> dict:
    if collection == 'individuals':
        for dict in INDIVIDUALS_FILTERS_MAP:
            for k, v in dict.items():
                v["$regex"] = f".*{filter.id}.*"
        search_dict={}
        search_dict["$or"] = INDIVIDUALS_FILTERS_MAP
        query = search_dict
        LOG.debug("QUERY: %s", query)
    elif collection == 'biosamples':
        for dict in BIOSAMPLES_FILTERS_MAP:
            for k, v in dict.items():
                v["$regex"] = f".*{filter.id}.*"
        search_dict={}
        search_dict["$or"] = BIOSAMPLES_FILTERS_MAP
        query = search_dict
        LOG.debug("QUERY: %s", query)
    elif collection == 'datasets':
        for dict in DATASETS_FILTERS_MAP:
            for k, v in dict.items():
                v["$regex"] = f".*{filter.id}.*"
        search_dict={}
        search_dict["$or"] = DATASETS_FILTERS_MAP
        query = search_dict
        LOG.debug("QUERY: %s", query)
    elif collection == 'g_variants':
        for dict in GENOMIC_VARIATIONS_FILTERS_MAP:
            for k, v in dict.items():
                v["$regex"] = f".*{filter.id}.*"
        search_dict={}
        search_dict["$or"] = GENOMIC_VARIATIONS_FILTERS_MAP
        query = search_dict
        LOG.debug("QUERY: %s", query)
    elif collection == 'runs':
        for dict in RUNS_FILTERS_MAP:
            for k, v in dict.items():
                v["$regex"] = f".*{filter.id}.*"
        search_dict={}
        search_dict["$or"] = RUNS_FILTERS_MAP
        query = search_dict
        LOG.debug("QUERY: %s", query)
    return query


def apply_custom_filter(query: dict, filter: CustomFilter) -> dict:
    LOG.debug(query)
    search_dict={}
    if "$text" in query:
        query["$text"]["$search"] += " "
    search_dict["$search"] = filter.id
    query["$text"] = search_dict
    LOG.debug("QUERY: %s", query)
    return query
