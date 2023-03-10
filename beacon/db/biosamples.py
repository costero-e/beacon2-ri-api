import logging
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.utils import query_id, query_ids, get_count, get_documents, get_cross_query
from beacon.db import client
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.db.filters import *
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import *
from beacon.request.model import RequestParams

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


def get_biosamples(entry_id: Optional[str], qparams: RequestParams):
    collection = 'biosamples'
    query = apply_request_parameters({}, qparams)
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


def get_biosample_with_id(entry_id: Optional[str], qparams: RequestParams):
    collection = 'biosamples'
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    schema = DefaultSchemas.BIOSAMPLES
    count = get_count(client.beacon.biosamples, query)
    docs = get_documents(
        client.beacon.biosamples,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_variants_of_biosample(entry_id: Optional[str], qparams: RequestParams):
    collection = 'biosamples'
    query = {"$and": [{"id": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    count = get_count(client.beacon.biosamples, query)
    biosamples_ids = client.beacon.biosamples \
        .find_one(query, {"id": 1, "_id": 0})
    LOG.debug(biosamples_ids)
    biosamples_ids=get_cross_query(biosamples_ids,'id','caseLevelData.biosampleId')
    LOG.debug(biosamples_ids)
    query = apply_filters(biosamples_ids, qparams.query.filters, collection)

    schema = DefaultSchemas.GENOMICVARIATIONS
    count = get_count(client.beacon.genomicVariations, query)
    docs = get_documents(
        client.beacon.genomicVariations,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_analyses_of_biosample(entry_id: Optional[str], qparams: RequestParams):
    collection = 'biosamples'
    query = {"biosampleId": entry_id}
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


def get_runs_of_biosample(entry_id: Optional[str], qparams: RequestParams):
    collection = 'biosamples'
    query = {"biosampleId": entry_id}
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
