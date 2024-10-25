import json
import os
import pprint
import unittest

from database import DatabaseEngine
from meta import MetadataParser

class TestDataBaseEngine(DatabaseEngine):
    _init_path = os.path.join(os.path.dirname(__file__), '../database/sql/init.sql')


cursor = TestDataBaseEngine.create()
TestDataBaseEngine.after_create(cursor)


class TestConsole(unittest.TestCase):
    __meta_data_path = os.path.join(os.path.dirname(__file__), 'resources/meta.json')

    def test_parse(self):
        parser = MetadataParser()
        with open(self.__meta_data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        parser.run(data)
        pprint.pprint(parser.build_tree())