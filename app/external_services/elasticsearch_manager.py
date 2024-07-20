from ..external_services.search_manager import SearchManager
from elasticsearch import Elasticsearch
from typing import Dict, List
from ..models.products import Products
from ..schemas.input_schema.pattern_input_schema import Pattern
from ..exceptions import DataUploadException


class ElasticSearchManager(SearchManager):

    DEFAULT_MAPPING = mappings = {
            "name": {"type": "text"},
            "min_qty": {"type": "number"},
            "max_qty": {"type": "number"},
            "description": {"type": "text"},
            "available": {"type": "number"}
    }

    def __init__(self, config):
        self.es = Elasticsearch(
            [f'{config["ELASTIC"]["scheme"]}://{config["ELASTIC"]["host"]}:{config["ELASTIC"]["port"]}'],  # Replace with your host
            verify_certs=False
        )
        self.index = config["ELASTIC"]["index"]

    def create_index(self, index_mapping=None):
        if not index_mapping:
            index_mapping = self.DEFAULT_MAPPING

        self.es.indices.create(index=self.index, body=index_mapping)

    def upload_documents_to_index(self, data: List[Products], index=''):
        if not index:
            index = self.index
        try:
            for document in data:
                self.es.index(
                    index=index,
                    id=document.id,
                    body={
                        "name": document.name,
                        "min_qty": document.min_qty,
                        "max_qty": document.max_qty,
                        "description": document.description,
                        "available": document.available
                    },
                )
        except DataUploadException as ex:
            raise ex
        return True

    def get_document_by_id(self, document_id):
        return self.es.get(index=self.index, id=document_id)

    def search(self, pattern=''):
        return self.es.search(index=self.index, body={"match": {"description": {"query": pattern}}})

    def get_documents_by_pattern(self, pattern: Pattern, spell_check_required=True, raw_response=False):
        request_body = dict(query=dict(fuzzy=dict()))
        if pattern.description:
            request_body["query"]["fuzzy"]["description"] = pattern.description
        if pattern.name:
            request_body["query"]["fuzzy"]["name"] = pattern.name
        response = self.es.search(index=self.index, body=request_body)
        if raw_response:
            return response
        return self.trim_response(response)

    @staticmethod
    def format_data(item):
        return item.get('_source')

    @staticmethod
    def trim_response(data: Dict):
        return data.get('hits', {}).get('hits', [])

