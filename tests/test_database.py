#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pytest tests.

    REQUIREMENTS:
    - mongodb server 4.2. By default it is assumed that mongodb is running on localhost.
"""

import os
import sys
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) +
                '/../tg_symstoremgr')

from database import SymbolsDatabase
COLLECTION = SymbolsDatabase(mongo_dbname='unittesting_tmp', collection_drop = True)
COLLECTION.data = [{
                        "guid": "3C431D2B32A332D800000000000000000",
                        "filename": "DedicatedServer",
                        "platform": "Linux",
                        "arch": "x86_64",
                        "symservers": ["breakpad"]
                    },{
                        "guid": "66E26DA26A11F18500000000000000000",
                        "filename": "ServiceContainer",
                        "platform": "Linux",
                        "arch": "x86_64",
                        "symservers": ["breakpad"]
                    }
                ]

def test_data_exist():
    assert COLLECTION.data[0]["guid"] == "3C431D2B32A332D800000000000000000"

def test_import_data():
    assert COLLECTION.import_data() is True

def test_update_symservers():
    result = COLLECTION.update_symservers(record=COLLECTION.data[0])
    assert result > 0

    query = {"guid": COLLECTION.data[0]["guid"]}
    res = COLLECTION.find(query=query)
    assert "symstore" in res[0]["symservers"]
