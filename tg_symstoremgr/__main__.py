#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""initially born by ID-103038.

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

if __package__:
    from .database import SymbolsDatabase
    from .datafile import SymbolsDataFile
    from .__init__ import __version__
else:
    from database import SymbolsDatabase
    from datafile import SymbolsDataFile
    from __init__ import __version__

def parse_args(args=None):
    """
    Define command-line arguments.

    args parameter is for unittests. It defines arguments values when unittesting.
    """

    parser = ArgumentParser(description=f"Symbols storages manager v{__version__}")
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


def main():
    ARGS = parse_args()

    if ARGS.task == 'import-from-datafiles':
        collection = SymbolsDatabase(mongo_addr     = ARGS.mongo_addr,
                                mongo_dbname   = ARGS.mongo_dbname)
        datafiles = glob.glob(ARGS.data_files)

        for datafile in datafiles:
            with open(datafile, 'r') as f:
                data = json.load(f)
            collection.data += add_data_fields(data)

        collection.import_data()


if __name__ == "__main__":
    main()
