from collections import defaultdict
from typing import List, Union
import re
import dataclasses
from copy import deepcopy

from beacon.request import ontologies
from beacon.request.model import AlphanumericFilter, CustomFilter, OntologyFilter, Operator, Similarity
from beacon.db.utils import get_documents
from beacon.db import client

import obonet

import logging

LOG = logging.getLogger(__name__)

CURIE_REGEX = r'^([a-zA-Z0-9]*):\/?[a-zA-Z0-9]*$'

INDIVIDUALS_MAP = ['diseases.diseaseCode.id', 'diseases.diseaseCode.label', 'ethnicity.id', 'ethnicity.label', 'geographicOrigin.id', 'geographicOrigin.label', 'id', 'info.eid', 'interventionsOrProcedures.procedureCode.id', 'interventionsOrProcedures.procedureCode.label', 'measures.assayCode.id', 'measures.assayCode.label', 'measures.date', 'measures.measurementValue.quantity.unit.id','measures.measurementValue.quantity.unit.label','measures.measurementValue.quantity.value','sex.id','sex.label']
ANALYSES_MAP = ['aligner', 'analysisDate', 'biosampleId', 'id', 'individualId', 'pipelineName', 'pipelineRef','runId', 'variantCaller']
BIOSAMPLES_MAP = ['biosampleStatus.id', 'biosampleStatus.label', 'collectionDate', 'collectionMoment', 'id', 'individualId', 'info.BioSamples.accession','info.BioSamples.externalUrl', 'info.EGAsampleId', 'info.characteristics.organism.ontologyTerms','info.characteristics.organism.text','info.sampleName','info.taxId','sampleOriginType.id','sampleOriginType.label']
G_VARIANTS_MAP = ['_info.vcf2bff.hostname', '_info.vcf2bff.filein', '_info.vcf2bff.user', '_info.vcf2bff.ncpuhost', '_info.vcf2bff.fileout', '_info.vcf2bff.cwd', '_info.vcf2bff.projectDir','_info.vcf2bff.version', '_info.datasetId', '_info.genome','caseLevelData.zygosity.label','caseLevelData.zygosity.id','caseLevelData.biosampleId','molecularAttributes.geneIds','molecularAttributes.annotationImpact','molecularAttributes.aminoacidChanges','molecularAttributes.molecularEffects.label','molecularAttributes.molecularEffects.id','variantQuality.FILTER','variantQuality.QUAL','_position.start','_position.end','_position.endInteger','_position.startInteger','_position.refseqId','_position.assemblyId','variation.variantType','variation.alternateBases','variation.referenceBases','variation.location.interval.start.value','variation.location.interval.start.type','variation.location.interval.end.value','variation.location.interval.end.type','variation.location.interval.type','variation.location.type','variation.location.sequence_id','variation.variantInternalId','variation.identifiers.genomicHGVSId']
RUNS_MAP = ['biosampleId','id','individualId','libraryLayout','librarySelection','librarySource.id','librarySource.label','libraryStrategy','platform','platformModel.id','platformModel.label','runDate']

def apply_filters(query: dict, filters: List[dict], collection: str) -> dict:
    LOG.debug("Filters len = {}".format(len(filters)))
    if len(filters) > 0:
        query["$and"] = []
    if len(filters) >= 1:
        for filter in filters:
            partial_query = {}
            if "value" in filter:
                LOG.debug(filter)
                filter = AlphanumericFilter(**filter)
                LOG.debug("Alphanumeric filter: %s %s %s", filter.id, filter.operator, filter.value)
                partial_query = apply_alphanumeric_filter(partial_query, filter, collection)
            elif "includeDescendantTerms" not in filter:
                filter=OntologyFilter(**filter)
                filter.include_descendant_terms=True
                LOG.debug("Ontology filter: %s", filter.id)
                #partial_query = {"$text": defaultdict(str) }
                #partial_query =  { "$text": { "$search": "" } } 
                LOG.debug(partial_query)
                partial_query = apply_ontology_filter(partial_query, filter, collection)
            elif "similarity" in filter or "includeDescendantTerms" in filter or re.match(CURIE_REGEX, filter["id"]):
                filter = OntologyFilter(**filter)
                LOG.debug("Ontology filter: %s", filter.id)
                #partial_query = {"$text": defaultdict(str) }
                #partial_query =  { "$text": { "$search": "" } } 
                LOG.debug(partial_query)
                partial_query = apply_ontology_filter(partial_query, filter, collection)
            else:
                filter = CustomFilter(**filter)
                LOG.debug("Custom filter: %s", filter.id)
                partial_query = apply_custom_filter(partial_query, filter, collection)
            query["$and"].append(partial_query)
    return query


def apply_ontology_filter(query: dict, filter: OntologyFilter, collection: str) -> dict:
    
    is_filter_id_required = True

    # Search similar
    if filter.similarity != Similarity.EXACT:
        cutoff = 1
        is_filter_id_required = False
        ontology_list=filter.id.split(':')
        if filter.similarity == Similarity.HIGH:
            similarity_high=[]
            path = "./beacon/similarities/{}{}{}.txt".format(ontology_list[0],ontology_list[1],'high')
            with open(path, 'r') as f:
                for line in f:
                    line = line.replace("\n","")
                    similarity_high.append(line)
            final_term_list = similarity_high
        elif filter.similarity == Similarity.MEDIUM:
            similarity_medium=[]
            path = "./beacon/similarities/{}{}{}.txt".format(ontology_list[0],ontology_list[1],'medium')
            with open(path, 'r') as f:
                for line in f:
                    line = line.replace("\n","")
                    similarity_medium.append(line)
            final_term_list = similarity_medium
        elif filter.similarity == Similarity.LOW:
            similarity_low=[]
            path = "./beacon/similarities/{}{}{}.txt".format(ontology_list[0],ontology_list[1],'low')
            with open(path, 'r') as f:
                for line in f:
                    line = line.replace("\n","")
                    similarity_low.append(line)
            final_term_list = similarity_low
        
        final_term_list.append(filter.id)
        query['$or']=[]
        for onto_query in final_term_list:
            if collection == 'individuals':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in INDIVIDUALS_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{onto_query}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'analyses':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in ANALYSES_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{onto_query}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'biosamples':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in BIOSAMPLES_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{onto_query}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'g_variants':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in G_VARIANTS_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{onto_query}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'runs':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in RUNS_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{onto_query}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)

    # Apply descendant terms
    if filter.include_descendant_terms == True:
        is_filter_id_required = False
        try:
            ontology=filter.id.replace("\n","")
            LOG.debug(ontology)
            ontology_list=ontology.split(':')
            list_descendant = []
            path = "./beacon/descendants/{}{}.txt".format(ontology_list[0],ontology_list[1])
            LOG.debug(path)
            with open(path, 'r') as f:
                for line in f:
                    line=line.replace("\n","")
                    list_descendant.append(line)
            query['$or']=[]
            list_descendant.append(filter.id)
            for desc in list_descendant:  
                if collection == 'individuals':
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    for item in INDIVIDUALS_MAP:
                        dict_filter_2={}
                        dict_filter_2[item]=''
                        dict_filter_2[item]+=f'{desc}'
                        dict_text_2['$or'].append(dict_filter_2)
                    query['$or'].append(dict_text_2)
                elif collection == 'analyses':
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    for item in ANALYSES_MAP:
                        dict_filter_2={}
                        dict_filter_2[item]=''
                        dict_filter_2[item]+=f'{desc}'
                        dict_text_2['$or'].append(dict_filter_2)
                    query['$or'].append(dict_text_2)
                elif collection == 'biosamples':
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    for item in BIOSAMPLES_MAP:
                        dict_filter_2={}
                        dict_filter_2[item]=''
                        dict_filter_2[item]+=f'{desc}'
                        dict_text_2['$or'].append(dict_filter_2)
                    query['$or'].append(dict_text_2)
                elif collection == 'g_variants':
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    for item in G_VARIANTS_MAP:
                        dict_filter_2={}
                        dict_filter_2[item]=''
                        dict_filter_2[item]+=f'{desc}'
                        dict_text_2['$or'].append(dict_filter_2)
                    query['$or'].append(dict_text_2)
                elif collection == 'runs':
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    for item in RUNS_MAP:
                        dict_filter_2={}
                        dict_filter_2[item]=''
                        dict_filter_2[item]+=f'{desc}'
                        dict_text_2['$or'].append(dict_filter_2)
                    query['$or'].append(dict_text_2)
        except Exception:
            query['$or']=[]
            if collection == 'individuals':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in INDIVIDUALS_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{filter.id}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'analyses':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in ANALYSES_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{filter.id}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'biosamples':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in BIOSAMPLES_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{filter.id}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'g_variants':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in G_VARIANTS_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{filter.id}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'runs':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in RUNS_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{filter.id}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)

    if is_filter_id_required:
            query['$or']=[]
            if collection == 'individuals':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in INDIVIDUALS_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{filter.id}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'analyses':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in ANALYSES_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{filter.id}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'biosamples':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in BIOSAMPLES_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{filter.id}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'g_variants':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in G_VARIANTS_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{filter.id}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
            elif collection == 'runs':
                dict_text_2={}
                dict_text_2['$or']=[]
                for item in RUNS_MAP:
                    dict_filter_2={}
                    dict_filter_2[item]=''
                    dict_filter_2[item]+=f'{filter.id}'
                    dict_text_2['$or'].append(dict_filter_2)
                query['$or'].append(dict_text_2)
    

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

def apply_alphanumeric_filter(query: dict, filter: AlphanumericFilter, collection: str) -> dict:
    LOG.debug(filter.value)
    formatted_value = format_value(filter.value)
    formatted_operator = format_operator(filter.operator)
    if collection == 'g_variants':
        formatted_value = format_value(filter.value)
        formatted_operator = format_operator(filter.operator)
        query[filter.id] = { formatted_operator: formatted_value }
    elif isinstance(formatted_value,str):
        if formatted_operator == "$eq":
            if '%' in filter.value:
                if collection == 'individuals':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    value_splitted=filter.value.split('%')
                    regex_dict={}
                    regex_dict['$regex']=value_splitted[1]
                    for item in INDIVIDUALS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=regex_dict
                        dict_text['$or'].append(dict_filter)
                    query['$and'].append(dict_text)
                    query['$and'].append(dict_text_2)
                elif collection == 'analyses':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    value_splitted=filter.value.split('%')
                    regex_dict={}
                    regex_dict['$regex']=value_splitted[1]
                    for item in ANALYSES_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=regex_dict
                        dict_text['$or'].append(dict_filter)
                    query['$and'].append(dict_text)
                    query['$and'].append(dict_text_2)
                elif collection == 'biosamples':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    value_splitted=filter.value.split('%')
                    regex_dict={}
                    regex_dict['$regex']=value_splitted[1]
                    for item in BIOSAMPLES_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=regex_dict
                        dict_text['$or'].append(dict_filter)
                    query['$and'].append(dict_text)
                    query['$and'].append(dict_text_2)
                elif collection == 'g_variants':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    value_splitted=filter.value.split('%')
                    regex_dict={}
                    regex_dict['$regex']=value_splitted[1]
                    for item in G_VARIANTS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=regex_dict
                        dict_text['$or'].append(dict_filter)
                    query['$and'].append(dict_text)
                    query['$and'].append(dict_text_2)
                elif collection == 'runs':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    value_splitted=filter.value.split('%')
                    regex_dict={}
                    regex_dict['$regex']=value_splitted[1]
                    for item in RUNS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=regex_dict
                        dict_text['$or'].append(dict_filter)
                    query['$and'].append(dict_text)
                    query['$and'].append(dict_text_2)
            else:
                if collection == 'individuals':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    for item in INDIVIDUALS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=filter.value
                        dict_text['$or'].append(dict_filter)
                    query['$and'].append(dict_text)
                    query['$and'].append(dict_text_2)
                elif collection == 'analyses':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    for item in ANALYSES_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=filter.value
                        dict_text['$or'].append(dict_filter)
                    query['$and'].append(dict_text)
                    query['$and'].append(dict_text_2)
                elif collection == 'biosamples':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    for item in BIOSAMPLES_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=filter.value
                        dict_text['$or'].append(dict_filter)
                    query['$and'].append(dict_text)
                    query['$and'].append(dict_text_2)
                elif collection == 'g_variants':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    for item in G_VARIANTS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=filter.value
                        dict_text['$or'].append(dict_filter)
                    query['$and'].append(dict_text)
                    query['$and'].append(dict_text_2)
                elif collection == 'runs':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    for item in RUNS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=filter.value
                        dict_text['$or'].append(dict_filter)
                    query['$and'].append(dict_text)
                    query['$and'].append(dict_text_2)
                    
        elif formatted_operator == "$ne":
            if '%' in filter.value:
                if collection == 'individuals':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    value_splitted=filter.value.split('%')
                    regex_dict={}
                    regex_dict['$regex']=value_splitted[1]
                    not_dict={}
                    not_dict['$not']=regex_dict
                    for item in INDIVIDUALS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=not_dict
                        query['$and'].append(dict_filter)
                    query['$and'].append(dict_text_2)
                elif collection == 'analyses':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    value_splitted=filter.value.split('%')
                    regex_dict={}
                    regex_dict['$regex']=value_splitted[1]
                    not_dict={}
                    not_dict['$not']=regex_dict
                    for item in ANALYSES_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=not_dict
                        query['$and'].append(dict_filter)
                    query['$and'].append(dict_text_2)
                elif collection == 'biosamples':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    value_splitted=filter.value.split('%')
                    regex_dict={}
                    regex_dict['$regex']=value_splitted[1]
                    not_dict={}
                    not_dict['$not']=regex_dict
                    for item in BIOSAMPLES_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=not_dict
                        query['$and'].append(dict_filter)
                    query['$and'].append(dict_text_2)
                elif collection == 'g_variants':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    value_splitted=filter.value.split('%')
                    regex_dict={}
                    regex_dict['$regex']=value_splitted[1]
                    not_dict={}
                    not_dict['$not']=regex_dict
                    for item in G_VARIANTS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=not_dict
                        query['$and'].append(dict_filter)
                    query['$and'].append(dict_text_2)
                elif collection == 'runs':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    value_splitted=filter.value.split('%')
                    regex_dict={}
                    regex_dict['$regex']=value_splitted[1]
                    not_dict={}
                    not_dict['$not']=regex_dict
                    for item in RUNS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=not_dict
                        query['$and'].append(dict_filter)
                    query['$and'].append(dict_text_2)
            else:
                if collection == 'individuals':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    regex_dict={}
                    regex_dict['$eq']=filter.value
                    not_dict={}
                    not_dict['$not']=regex_dict
                    for item in INDIVIDUALS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=not_dict
                        query['$and'].append(dict_filter)
                    query['$and'].append(dict_text_2)
                elif collection == 'analyses':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    regex_dict={}
                    regex_dict['$eq']=filter.value
                    not_dict={}
                    not_dict['$not']=regex_dict
                    for item in ANALYSES_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=not_dict
                        query['$and'].append(dict_filter)
                    query['$and'].append(dict_text_2)
                elif collection == 'biosamples':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    regex_dict={}
                    regex_dict['$eq']=filter.value
                    not_dict={}
                    not_dict['$not']=regex_dict
                    for item in BIOSAMPLES_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=not_dict
                        query['$and'].append(dict_filter)
                    query['$and'].append(dict_text_2)
                elif collection == 'g_variants':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    regex_dict={}
                    regex_dict['$eq']=filter.value
                    not_dict={}
                    not_dict['$not']=regex_dict
                    for item in G_VARIANTS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=not_dict
                        query['$and'].append(dict_filter)
                    query['$and'].append(dict_text_2)
                elif collection == 'runs':
                    query['$and']=[]
                    dict_text={}
                    dict_text['$or']=[]
                    dict_text_2={}
                    dict_text_2['$or']=[]
                    regex_dict={}
                    regex_dict['$eq']=filter.value
                    not_dict={}
                    not_dict['$not']=regex_dict
                    for item in RUNS_MAP:
                        dict_filter={}
                        dict_filter_2={}
                        dict_filter_2[item]=filter.id
                        dict_text_2['$or'].append(dict_filter_2)
                        dict_filter[item]=not_dict
                        query['$and'].append(dict_filter)
                    query['$and'].append(dict_text_2)
    else:
        query['measurementValue.quantity.value'] = { formatted_operator: float(formatted_value) }
        query['assayCode.id']=filter.id
        LOG.debug(query)
        dict_elemmatch={}
        dict_elemmatch['$elemMatch']=query
        dict_measures={}
        dict_measures['measures']=dict_elemmatch
        query = dict_measures


    LOG.debug("QUERY: %s", query)
    return query



def apply_custom_filter(query: dict, filter: CustomFilter, collection:str) -> dict:
    LOG.debug(query)
    query['$or']=[]
    if collection == 'individuals':
        dict_text_2={}
        dict_text_2['$or']=[]
        for item in INDIVIDUALS_MAP:
            dict_filter_2={}
            dict_filter_2[item]=''
            dict_filter_2[item]+=f'{filter.id}'
            dict_text_2['$or'].append(dict_filter_2)
        query['$or'].append(dict_text_2)
    elif collection == 'analyses':
        dict_text_2={}
        dict_text_2['$or']=[]
        for item in ANALYSES_MAP:
            dict_filter_2={}
            dict_filter_2[item]=''
            dict_filter_2[item]+=f'{filter.id}'
            dict_text_2['$or'].append(dict_filter_2)
        query['$or'].append(dict_text_2)
    elif collection == 'biosamples':
        dict_text_2={}
        dict_text_2['$or']=[]
        for item in BIOSAMPLES_MAP:
            dict_filter_2={}
            dict_filter_2[item]=''
            dict_filter_2[item]+=f'{filter.id}'
            dict_text_2['$or'].append(dict_filter_2)
        query['$or'].append(dict_text_2)
    elif collection == 'g_variants':
        dict_text_2={}
        dict_text_2['$or']=[]
        for item in G_VARIANTS_MAP:
            dict_filter_2={}
            dict_filter_2[item]=''
            dict_filter_2[item]+=f'{filter.id}'
            dict_text_2['$or'].append(dict_filter_2)
        query['$or'].append(dict_text_2)
    elif collection == 'runs':
        dict_text_2={}
        dict_text_2['$or']=[]
        for item in RUNS_MAP:
            dict_filter_2={}
            dict_filter_2[item]=''
            dict_filter_2[item]+=f'{filter.id}'
            dict_text_2['$or'].append(dict_filter_2)
        query['$or'].append(dict_text_2)

    LOG.debug("QUERY: %s", query)
    return query
