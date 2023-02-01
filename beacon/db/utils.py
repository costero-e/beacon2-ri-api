from typing import Dict, Optional

from pymongo.cursor import Cursor
from pymongo.collection import Collection
from beacon.db import client
from beacon.request.model import RequestParams
import logging

LOG = logging.getLogger(__name__)


def query_id(query: dict, document_id) -> dict:
    query["id"] = document_id
    return query


def query_ids(query: dict, ids) -> dict:
    query["id"] = ids
    return query


def query_property(query: dict, property_id: str, value: str, property_map: Dict[str, str]) -> dict:
    query[property_map[property_id]] = value
    return query


def get_count(collection: Collection, query: dict) -> int:
    if not query:
        LOG.debug("Returning estimated count")
        return collection.estimated_document_count()
    else:
        LOG.debug("FINAL QUERY (COUNT): {}".format(query))
        LOG.debug("Returning count")
        return collection.count_documents(query)


def get_documents(collection: Collection, query: dict, skip: int, limit: int) -> Cursor:
    LOG.debug("FINAL QUERY: {}".format(query))
    return collection.find(query).skip(skip).limit(limit).max_time_ms(10 * 1000)

def get_cross_query(ids: dict, cross_type: str, collection_id: str):
    id_list=[]
    dict_in={}
    id_dict={}
    if cross_type != 'single':
        for k, v in ids.items():
            for item in v:
                id_list.append(item[cross_type])
        dict_in["$in"]=id_list

    else:
        list_item=ids[collection_id]
        LOG.debug(str(list_item))
        id_list.append(str(list_item))
        dict_in["$in"]=id_list
        LOG.debug(id_list)
    id_dict[collection_id]=dict_in
    query = id_dict
    LOG.debug(query)
    return query
