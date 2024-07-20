from typing import Dict, List
import requests
from ..external_services.search_manager import SearchManager
from ..exceptions import DataUploadException, InvalidInput
import json


class SolrManager(SearchManager):

    default_headers = {'Content-Type': 'application/json'}

    def __init__(self, config):
        self.solr_base_url = f"{config['SOLR']['scheme']}://{config['SOLR']['host']}:{config['SOLR']['port']}/solr/{config['SOLR']['core']}/"

    def create_index(self, index_mapping=None):
        # Solr provides an easy UI for creating index and there is a need to create solr config and schema files as well
        # for this which is a manual process so keeping this as a placeholder implementation of the base class
        pass

    def upload_documents_to_index(self, data: List, index=""):
        data_json = []
        for item in data:
            data_json.append(dict(id=item.id,
                                  name=self.preprocess_field(item.name),
                                  min_qty=item.min_qty,
                                  max_qty=item.max_qty,
                                  description=self.preprocess_field(item.description),
                                  available=item.available))
        response = requests.post(self.solr_base_url + 'update' + '?commit=true', data=json.dumps(data_json), headers=self.default_headers)
        response = response.json()

        if response.get('responseHeader', {}).get('status') == 0:
            return True
        raise DataUploadException()

    def get_document_by_id(self, document_id):
        response = requests.get(self.solr_base_url + 'select' + '?q=id:' + str(document_id))
        response = response.json()
        return response

    def search(self, pattern=''):
        response = requests.get(self.solr_base_url + 'select' + '?q=description:' + '*' + self.preprocess_field(pattern) + '*')
        response = response.json()
        return response

    def get_documents_by_pattern(self, pattern, spell_check_required=True, raw_response=False):
        if spell_check_required:
            self.validate_words(pattern)

        url = self.solr_base_url + 'select' + '?q='
        if pattern.description:
            url += ('description' + ':' + '*' + self.preprocess_field(pattern.description) + '*')
        if pattern.description and pattern.name:
            url += ' AND '
        if pattern.name:
            url += ('name' + ':' + '*' + self.preprocess_field(pattern.name) + '*')
        response = requests.get(url)
        response = response.json()
        if raw_response:
            return response
        return self.trim_response(response)

    @staticmethod
    def format_data(item):
        return item

    @staticmethod
    def trim_response(data: Dict):
        return data.get('response', {}).get('docs')

    @staticmethod
    def preprocess_field(field: str):
        return field.lower()

    def validate_words(self, pattern):
        """
        Preprocessing for spell checking
        :param pattern: Pattern object
        """
        words = set()
        if pattern.description:
            words.add(pattern.description)
        if pattern.name:
            words.add(pattern.name)

        for word in words:
            result = self.spell_check(word)
            if type(result) is set:
                raise InvalidInput(result)
