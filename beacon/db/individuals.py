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

INDIVIDUALS_PROPERTY_MAP = {
    "diseaseId": "diseases.diseaseCode.id",
    "diseaseLabel": "diseases.diseaseCode.label",
    "ethnicityId": "ethnicity.id",
    "ethnicityLabel": "ethnicity.label",
    "geographicOriginId": "geographicOrigin.id",
    "geographicOriginLabel": "geographicOrigin.label",
    "assayCodeId": "measures.assayCode.id",
    "assayCodeLabel": "measures.assayCode.label",
    "date": "measures.date",
    "measurementValueId": "measures.measurementValue.quantity.unit.id",
    "measurementValueLabel": "measures.measurementValue.quantity.unit.label",
    "measurementValue": "measures.measurementValue.quantity.value",
    "sexId": "sex.id",
    "sexLabel": "sex.label"
}

def generate_position_filter_start(key: str, value: List[int]) -> List[AlphanumericFilter]:
    LOG.debug("len value = {}".format(len(value)))
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=INDIVIDUALS_PROPERTY_MAP[key],
            value=[value[0]],
            operator=Operator.GREATER_EQUAL
        ))
    elif len(value) == 2:
        filters.append(AlphanumericFilter(
            id=INDIVIDUALS_PROPERTY_MAP[key],
            value=[value[0]],
            operator=Operator.GREATER_EQUAL
        ))
        filters.append(AlphanumericFilter(
            id=INDIVIDUALS_PROPERTY_MAP[key],
            value=[value[1]],
            operator=Operator.LESS_EQUAL
        ))
    return filters


def generate_position_filter_end(key: str, value: List[int]) -> List[AlphanumericFilter]:
    LOG.debug("len value = {}".format(len(value)))
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=INDIVIDUALS_PROPERTY_MAP[key],
            value=[value[0]],
            operator=Operator.LESS_EQUAL
        ))
    elif len(value) == 2:
        filters.append(AlphanumericFilter(
            id=INDIVIDUALS_PROPERTY_MAP[key],
            value=[value[0]],
            operator=Operator.GREATER_EQUAL
        ))
        filters.append(AlphanumericFilter(
            id=INDIVIDUALS_PROPERTY_MAP[key],
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
                id=INDIVIDUALS_PROPERTY_MAP[k],
                value=v
            )))
    return query

def get_individuals(entry_id: Optional[str], qparams: RequestParams):
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters)
    print(query)
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
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters)
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
    query = {"$and": [{"id": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters)
    count = get_count(client.beacon.individuals, query)
    individual_ids = client.beacon.individuals \
        .find_one(query, {"id": 1, "_id": 0})
    LOG.debug(individual_ids)
    individual_ids=get_cross_query(individual_ids,'id','caseLevelData.biosampleId')
    LOG.debug(individual_ids)
    query = apply_filters(individual_ids, qparams.query.filters)

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
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters)
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
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters)
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
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters)
    schema = DefaultSchemas.ANALYSES
    count = get_count(client.beacon.analyses, query)
    docs = get_documents(
        client.beacon.analyses,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs
