import json
import asyncio
import logging
from aiohttp import web
from aiohttp.web_request import Request
from bson import json_util
from beacon import conf

from beacon.request import ontologies
from beacon.request.model import Granularity, RequestParams
from beacon.response.build_response import (
    build_beacon_resultset_response,
    build_beacon_collection_response,
    build_beacon_boolean_response,
    build_beacon_count_response,
    build_filtering_terms_response,
)
from beacon.utils.stream import json_stream
from beacon.db.datasets import get_datasets
from beacon.utils.auth import resolve_token

LOG = logging.getLogger(__name__)


def collection_handler(db_fn, request=None):
    async def wrapper(request: Request):
        # Get params
        json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
        qparams = RequestParams(**json_body).from_request(request)
        entry_id = request.match_info["id"] if "id" in request.match_info else None

        # Get response
        entity_schema, count, records = db_fn(entry_id, qparams)
        response_converted = (
            [r for r in records] if records else []
        )
        response = build_beacon_collection_response(
            response_converted, count, qparams, lambda x, y: x, entity_schema
        )
        return await json_stream(request, response)

    return wrapper


def generic_handler(db_fn, request=None):
    async def wrapper(request: Request):
        # Get params
        json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
        qparams = RequestParams(**json_body).from_request(request)
        entry_id = request.match_info.get('id', None)

        # Get response

        
        _, _, datasets = get_datasets(None, qparams)
        beacon_datasets = [ r for r in datasets ]

        all_datasets = [ r['_id'] for r in beacon_datasets]
        specific_datasets = [ r['id'] for r in beacon_datasets]
        biosample_ids_disallowed = []
        access_token = request.headers.get('Authorization')
        authenticated=False
        LOG.debug(access_token)
        if access_token is not None:
            access_token = access_token[7:]  # cut out 7 characters: len('Bearer ')
            authorized_datasets, authenticated = await resolve_token(access_token, all_datasets)
            LOG.debug(authorized_datasets)
            LOG.debug('all datasets:  %s', all_datasets)
            LOG.info('resolved datasets:  %s', authorized_datasets)
            LOG.debug(authorized_datasets)
            
            

            for element in specific_datasets:
                if element not in authorized_datasets:
                    specific_datasets_unauthorized = [ r for r in beacon_datasets if r['id'] == element]
                    biosample_ids = [ r['ids'] for r in specific_datasets_unauthorized]
                            
                    for biosample_id in biosample_ids:
                        for bio_id in biosample_id['biosampleIds']:
                            biosample_ids_disallowed.append(bio_id)
            LOG.debug(biosample_ids_disallowed)
            


        entity_schema, count, records = db_fn(entry_id, qparams, biosample_ids_disallowed)

        response_converted = records
        
        if qparams.query.requested_granularity == Granularity.BOOLEAN:
            response = build_beacon_boolean_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
        
        elif qparams.query.requested_granularity == Granularity.COUNT:
            if conf.max_beacon_granularity == Granularity.BOOLEAN:
                response = build_beacon_boolean_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
            else:
                response = build_beacon_count_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
        
        # qparams.query.requested_granularity == Granularity.RECORD:
        else:

            if conf.max_beacon_granularity == Granularity.BOOLEAN:
                response = build_beacon_boolean_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
            elif conf.max_beacon_granularity == Granularity.COUNT:
                response = build_beacon_count_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
            else:
                response = build_beacon_resultset_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
                
        return await json_stream(request, response)

    return wrapper

def filtering_terms_handler(db_fn, request=None):
    async def wrapper(request: Request):
        # Get params
        json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
        qparams = RequestParams(**json_body).from_request(request)
        entry_id = request.match_info.get('id', None)

        # Get response
        _, _, records = db_fn(entry_id, qparams)
        resources = ontologies.get_resources()
        response = build_filtering_terms_response(records, resources, qparams)
        return await json_stream(request, response)

    return wrapper
