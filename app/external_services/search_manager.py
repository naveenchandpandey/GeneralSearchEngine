from abc import ABC, abstractmethod
from typing import List, Dict
from spellchecker import SpellChecker


class SearchManager(ABC):

    spell_checker = SpellChecker()

    @abstractmethod
    def create_index(self, index_mapping=None):
        """
        Used to create a new index in the search engine
        :param index_mapping: in case a mapping is required to create index
        """
        pass

    @abstractmethod
    def upload_documents_to_index(self, data: List, index=""):
        """
        Insert bulk data in to index
        :param data: List of objects to be uploaded
        :param index: index name in which it should be uploaded
        """
        pass

    @abstractmethod
    def get_document_by_id(self, document_id):
        """
        Fetches a document from search engine based on ID
        :param document_id: document ID in the search engine
        """
        pass

    @abstractmethod
    def search(self, pattern=''):
        """
        Search on the nosql db based on pattern object
        :param pattern: Pattern object
        """
        pass

    @abstractmethod
    def get_documents_by_pattern(self, pattern, raw_response=False):
        """
        Get results from search engine based on multiple pattern attributes
        :param pattern: Pattern object
        :param raw_response: Whether raw response form the engine is required
        """
        pass

    @staticmethod
    @abstractmethod
    def trim_response(data: Dict):
        """
        Removes unnecessary keys from response
        :param data: response object
        """
        pass

    def spell_check(self, word: str):
        """
        Provides spell checking functionality and also provides possible corrections
        :param word: word to be checked
        :return: True if spelling is correct, possible suggestions otherwise
        """
        if word == self.spell_checker.correction(word):
            return True
        return self.spell_checker.candidates(word)
