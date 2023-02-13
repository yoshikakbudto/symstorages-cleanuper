#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
initially born by ID-103038

The script manages symbols rotation

Known bugs/features
- When importing datafiles, there is no check for duplicate documents.
"""

from argparse import ArgumentParser
import datetime
import glob
import logging
import os
import json

from pymongo import MongoClient

def parse_args(args=None):
    """
    Define command-line arguments.

    args parameter is for unittests. It defines arguments values when unittesting.
    """
    parser = ArgumentParser(prog=os.path.basename(__file__),
                            description="Symbols cleanuper")
    parser.add_argument("--task", required=True,
                        choices=['import-from-datafiles'],
                        help="MongoDb address")
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help="Be more verbose. More -v increases verbosity,"
                             "i.e.: -vv will set loglevel to DEBUG. By default loglevel is WARNING")
    parser.add_argument("--mongo-addr", required=False, default="localhost",
                        help="MongoDb address")
    parser.add_argument("--mongo-dbname", required=False, default="symbols_dev",
                        help="MongoDb database")
    parser.add_argument("--data-files", required=False, default="symstore-cleanuper-*.json",
                        help="A filemask of a source data files. Default is: 'symstore-cleanuper-*.json'")


    parsed = parser.parse_args(args, namespace=None)

    # set loglevel (by default its warning) and simplify format
    logging.basicConfig(format='[%(levelname)s] %(message)s')
    if parsed.verbose == 2:
        logging.getLogger().setLevel(logging.DEBUG)
    elif parsed.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)

    return parsed


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


def add_data_fields(data):
    """Add some more fields to a document."""
    if type(data) is list:
        for i in data:
            i['timestamp'] = datetime.datetime.utcnow()
            if os.getenv('BUILD_NUMBER'):
                i['build_number'] = os.getenv('BUILD_NUMBER')
            if os.getenv('BuildBranch'):
                i['branch'] = os.getenv('BuildBranch')
    return data


if __name__ == "__main__":
    ARGS = parse_args()

    collection = SymbolsDatabase(mongo_addr     = ARGS.mongo_addr,
                                 mongo_dbname   = ARGS.mongo_dbname)

    if ARGS.task == 'import-from-datafiles':
        datafiles = glob.glob(ARGS.data_files)
        for datafile in datafiles:
            with open(datafile, 'r') as f:
                data = json.load(f)
            collection.data += add_data_fields(data)

        collection.import_data()
