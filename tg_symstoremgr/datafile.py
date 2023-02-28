#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ID-103038: The class is used for generating "symbols cleanuper" datafiles.

It should be used for every binary that stores its symbols on symbol server.
Later the provided metainfo we'll be used by the symbols server cleanup process

All platforms-specific configuration should be stored in here.

Known bugs and features:
- if os.getenv didnt find the variable, the key and its value (None/null) will not be stored in datafile.

"""

import os
import json
import logging

class SymbolsDataFile():
    # Valid document fields
    allowed_fields = {
        'symservers':           {'type': [] },
        'guid':                 {'type': '' },
        'filename':             {'type': '' },
        'platform':             {'type': '' },
        'arch':                 {'type': '' },
        'sdk_dir':              {'type': '' }
    }

    # symbols metadata
    data: list

    # json-filename that stores symbols metadata
    datafile: str

    # symbol's executable file platform (pc/ps4/etc...)
    platform: str

    def __init__(self, platform, data=[]):
        self.data = data
        self.platform = platform
        self.datafile = f'symstore-cleanuper-{self.platform}.json'

    def append(self, document):
        """Validate and add symbols metadata document."""
        validated_document = dict()

        for k,v in document.items():
            # check if key is valid
            if not k in self.allowed_fields:
                raise KeyError(f'field "{k}" is unknown. Please check the class {self.__class__.__name__} -> allowed_fields')

            # value may be 'None' if os.getenv didnt found the variable.
            if v:
                if type(self.allowed_fields[k]['type']) != type(v):
                    raise TypeError(f'the type of field "{k}" shoud be {type(self.allowed_fields[k]["type"])} (it is {type(v)} now)')
                validated_document[k]=v

        self.data.append(validated_document)

    def dumpdata(self):
        """Write symbols metadata to a json file."""
        if self.data:
            with open(self.datafile,'w') as f:
                f.write(json.dumps(self.data))

    def loadfromdatafile(self, ignoreerrors=True):
        """Load data from previouselly created datafile."""
        if os.path.isfile(self.datafile):
            with open(self.datafile,'r') as f:
                try:
                    self.data = json.load(f)
                except Exception as e:
                    if  ignoreerrors:
                        print(f'[warn] there were errors loading {self.datafile}: \n{e}')
                    else:
                        raise
