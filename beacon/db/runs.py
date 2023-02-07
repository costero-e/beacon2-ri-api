import logging
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.utils import query_id, query_ids, get_count, get_documents, get_cross_query
from beacon.db import client
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents
from beacon.request.model import RequestParams

LOG = logging.getLogger(__name__)

RUNS_PROPERTY_MAP = {
    "biosampleId": "biosampleId",
    "individualId": "individualId",
    "libraryLayout": "libraryLayout",
    "librarySelection": "librarySelection",
    "librarySourceId": "librarySource.id",
    "librarySourceLabel": "librarySource.label",
    "libraryStrategy": "libraryStrategy",
    "platform": "platform",
    "platformModelId": "platformModel.id",
    "platformModelLabel": "platformModel.label",
    "runDate": "runDate"
}

def generate_position_filter_start(key: str, value: List[int]) -> List[AlphanumericFilter]:
    LOG.debug("len value = {}".format(len(value)))
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=RUNS_PROPERTY_MAP[key],
            value=[value[0]],
            operator=Operator.GREATER_EQUAL
        ))
    elif len(value) == 2:
        filters.append(AlphanumericFilter(
            id=RUNS_PROPERTY_MAP[key],
            value=[value[0]],
            operator=Operator.GREATER_EQUAL
        ))
        filters.append(AlphanumericFilter(
            id=RUNS_PROPERTY_MAP[key],
            value=[value[1]],
            operator=Operator.LESS_EQUAL
        ))
    return filters


def generate_position_filter_end(key: str, value: List[int]) -> List[AlphanumericFilter]:
    LOG.debug("len value = {}".format(len(value)))
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=RUNS_PROPERTY_MAP[key],
            value=[value[0]],
            operator=Operator.LESS_EQUAL
        ))
    elif len(value) == 2:
        filters.append(AlphanumericFilter(
            id=RUNS_PROPERTY_MAP[key],
            value=[value[0]],
            operator=Operator.GREATER_EQUAL
        ))
        filters.append(AlphanumericFilter(
            id=RUNS_PROPERTY_MAP[key],
            value=[value[1]],
            operator=Operator.LESS_EQUAL
        ))
    return filters


def apply_request_parameters(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Request parameters len = {}".format(len(qparams.query.request_parameters)))
    if len(qparams.query.request_parameters) > 0 and "$and" not in query:
        query["$and"] = []
    for k, v in qparams.query.request_parameters.items():
        query["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                id=RUNS_PROPERTY_MAP[k],
                value=v
            )))
    return query

def get_runs(entry_id: Optional[str], qparams: RequestParams):
    collection = 'runs'
    query = apply_request_parameters({}, qparams)
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


def get_run_with_id(entry_id: Optional[str], qparams: RequestParams):
    collection = 'runs'
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    schema = DefaultSchemas.RUNS
    count = get_count(client.beacon.runs, query)
    docs = get_documents(
        client.beacon.runs,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_variants_of_run(entry_id: Optional[str], qparams: RequestParams):
    collection = 'runs'
    query = {"$and": [{"id": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    count = get_count(client.beacon.runs, query)
    run_ids = client.beacon.runs \
        .find_one(query, {"biosampleId": 1, "_id": 0})
    run_ids=get_cross_query(run_ids,'biosampleId','caseLevelData.biosampleId')
    query = apply_filters(run_ids, qparams.query.filters, collection)

    schema = DefaultSchemas.GENOMICVARIATIONS
    count = get_count(client.beacon.genomicVariations, query)
    docs = get_documents(
        client.beacon.genomicVariations,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_analyses_of_run(entry_id: Optional[str], qparams: RequestParams):
    collection = 'runs'
    query = {"runId": entry_id}
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
