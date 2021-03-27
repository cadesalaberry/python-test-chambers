import os
import json
from django.test import TestCase


class JsonClientTestCase(TestCase):
        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            this_dir = os.path.dirname(__file__)
            sample_data_file_path = os.path.join(this_dir, '../../sample_data.json')
            with open(sample_data_file_path, 'rt', encoding='utf-8') as sample_data:
                cls.assets = json.loads(sample_data.read())
