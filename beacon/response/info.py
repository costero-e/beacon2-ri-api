"""
Info Endpoint.

Querying the info endpoint reveals information about this beacon and its existing datasets 
and their associated metadata.

* ``/`` Beacon-v1
* ``/info`` Beacon-v1
* ``/info?model=GA4GH-ServiceInfo-v0.1`` GA4GH
* ``/service-info`` GA4GH

"""

import logging
import json
from aiohttp.web_request import Request
from beacon.db.datasets import get_datasets
from beacon.request import RequestParams
from beacon.response.build_response import build_beacon_info_response
from beacon.utils.auth import resolve_token
from beacon.utils.stream import json_stream
from bson import json_util

LOG = logging.getLogger(__name__)

async def handler(request: Request):
    LOG.info('Running a GET info request')

    # Fetch datasets info
    json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
    qparams = RequestParams(**json_body).from_request(request)
    _, _, datasets = get_datasets(None, qparams)
    beacon_datasets = [ r for r in datasets ]

    all_datasets = [ r['_id'] for r in beacon_datasets]
    specific_datasets = [ r['id'] for r in beacon_datasets]
    biosample_ids_disallowed = []
    authenticated=False
    access_token = request.headers.get('Authorization')
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
        
    response_converted = build_beacon_info_response(beacon_datasets,
                                                                qparams,
                                                                lambda x,y,z: x,
                                                                authorized_datasets if authenticated else [])
    return await json_stream(request, response_converted)
