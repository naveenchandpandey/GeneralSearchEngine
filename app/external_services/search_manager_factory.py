from enum import Enum
from ..external_services.elasticsearch_manager import ElasticSearchManager
from ..external_services.solr_manager import SolrManager
from ..exceptions.custom_exceptions import InvalidManagerType


class SearchManagerFactory:

    class ManagerType(Enum):
        ELASTIC = 'ELASTIC'
        SOLR = 'SOLR'

    def __init__(self, config):
        """
        SearchManager factory provides instance of a particular search engine based on input parameter
        :param config: config object of the application configuration file
        """
        self.config = config

    def get_search_manager(self, manager_type):
        """
        Provides search engine instance based on manager_type
        :param manager_type: Defines which search manger to be used in the system
        :return: SearchManager object
        """
        if manager_type == SearchManagerFactory.ManagerType.ELASTIC.value:
            return ElasticSearchManager(self.config)
        elif manager_type == SearchManagerFactory.ManagerType.SOLR.value:
            return SolrManager(self.config)
        else:
            raise InvalidManagerType()
