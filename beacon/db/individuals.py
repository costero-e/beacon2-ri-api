import logging
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.utils import query_id, query_ids, get_count, get_documents, get_cross_query
from beacon.db import client
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents
from beacon.request.model import RequestParams
import json
from bson import json_util

LOG = logging.getLogger(__name__)


def apply_request_parameters(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Request parameters len = {}".format(len(qparams.query.request_parameters)))
    for k, v in qparams.query.request_parameters.items():
        query["$text"] = {}
        if ',' in v:
            v_list = v.split(',')
            v_string=''
            for val in v_list:
                v_string += f'"{val}"'
            query["$text"]["$search"]=v_string
        else:
            query["$text"]["$search"]=v
    return query


def get_individuals(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    schema = DefaultSchemas.INDIVIDUALS
    count = get_count(client.beacon.individuals, query)
    docs = get_documents(
        client.beacon.individuals,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_individual_with_id(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    schema = DefaultSchemas.INDIVIDUALS
    count = get_count(client.beacon.individuals, query)
    docs = get_documents(
        client.beacon.individuals,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_variants_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"$and": [{"id": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    count = get_count(client.beacon.individuals, query)
    individual_ids = client.beacon.individuals \
        .find_one(query, {"id": 1, "_id": 0})
    LOG.debug(individual_ids)
    individual_ids=get_cross_query(individual_ids,'id','caseLevelData.biosampleId')
    LOG.debug(individual_ids)
    query = apply_filters(individual_ids, qparams.query.filters, collection)

    schema = DefaultSchemas.GENOMICVARIATIONS
    count = get_count(client.beacon.genomicVariations, query)
    docs = get_documents(
        client.beacon.genomicVariations,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_biosamples_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    schema = DefaultSchemas.BIOSAMPLES
    count = get_count(client.beacon.biosamples, query)
    docs = get_documents(
        client.beacon.biosamples,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_filtering_terms_of_individual(entry_id: Optional[str], qparams: RequestParams):
    # TODO
    pass


def get_runs_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    schema = DefaultSchemas.RUNS
    count = get_count(client.beacon.runs, query)
    docs = get_documents(
        client.beacon.runs,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_analyses_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    schema = DefaultSchemas.ANALYSES
    count = get_count(client.beacon.analyses, query)
    docs = get_documents(
        client.beacon.analyses,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs
