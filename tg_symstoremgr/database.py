"""The class to manage database."""

import logging
from pymongo import MongoClient

class SymbolsDatabase:
    """Manages symbols metainfo in MongoDb"""

    data: list

    def __init__(self, mongo_addr='localhost', mongo_dbname='symbols_dev', collection_name = 'symbols', collection_drop = False):
        """Init constructor.
            Initializes the self.collection object
        """
        serverSelectionTimeoutMS = 5000

        c = MongoClient(host=f"mongodb://{mongo_addr}/{mongo_dbname}", serverSelectionTimeoutMS=serverSelectionTimeoutMS)
        client = c[mongo_dbname]
        self.collection = client[collection_name]

        if collection_drop:
            logging.info('dropping collection...')
            self.collection.drop()


    def import_data(self):
        self.__insert_many(self.data)
        return True


    def __insert_many(self, documents):
        """Insert a document list."""
        logging.debug(f'inserting documents: \n{documents}')
        self.collection.insert_many(documents)


    def update_symservers(self, record={}, match_field='guid'):
        """Update the given document with the given record."""

        record['symservers'].append('symstore')
        newvalues = { "$set": { 'symservers': record['symservers'] } }
        result = self.collection.update_one({match_field: record[match_field]}, newvalues)
        if result.matched_count > 0:
            logging.info(f"updated [{record[match_field]}] symservers: {record['symservers']}")
        else:
            logging.warning(f"document with _id:{record[match_field]} wasnt found in database. skip update")
        return result.matched_count

    def find(self, query={}, projection={}):
        return self.collection.find(query, projection)
