"""The class to manage database."""

import logging
from pymongo import MongoClient

class SymbolsDatabase:
    """Manages symbols metainfo in MongoDb"""

    data = []

    def __init__(self, mongo_addr='localhost', mongo_dbname='symbols_dev', collection_name = 'symbols'):
        """Init constructor.
            Initializes the self.collection object
        """
        serverSelectionTimeoutMS = 5000

        c = MongoClient(host=f"mongodb://{mongo_addr}/{mongo_dbname}", serverSelectionTimeoutMS=serverSelectionTimeoutMS)
        client = c[mongo_dbname]
        self.collection = client[collection_name]


    def import_data(self):
        self.__insert_many(self.data)


    def __insert_many(self, documents):
        """Insert a document list."""
        logging.debug(f'inserting documents: \n{documents}')
        self.collection.insert_many(documents)


    def update_server_types(self, record={}):
        """Update the given document with the given record."""

        record['server_types'].append('symstore')
        newvalues = { "$set": { 'server_types': record['server_types'] } }
        result = self.collection.update_one({'_id': record['_id']}, newvalues)
        if result.matched_count > 0:
            logging.info(f"updated [{record['_id']}] server_types: {record['server_types']}")
        else:
            logging.warning(f"document with _id:{record['_id']} wasnt found in database. skip update")



