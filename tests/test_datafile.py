#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pytest tests.

    REQUIREMENTS:
    - mongodb server 4.2. By default it is assumed that mongodb is running on localhost.
"""

import os
import sys
import pytest
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) +
                '/../tg_symstoremgr')

from datafile import SymbolsDataFile

METADATA = SymbolsDataFile(platform='test')


def test_datafile_append():
    document = {"arch": "x86_64"}
    METADATA.append(document)
    assert METADATA.data[0]["arch"] == "x86_64"

    document = {"invalid_field": "sdf"}
    with pytest.raises(KeyError):
        METADATA.append(document)

    document = {"guid": 123}
    with pytest.raises(TypeError):
        METADATA.append(document)

    document = {"symservers": "microsoft"}
    with pytest.raises(TypeError):
        METADATA.append(document)

def test_datafile_dumpdata():
    pass